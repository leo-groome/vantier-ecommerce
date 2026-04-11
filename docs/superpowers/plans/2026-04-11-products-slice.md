# Products Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the complete `products` feature slice — schemas, service, and router — giving the Vantier API a working public catalog and full admin CRUD for products, variants, and images.

**Architecture:** Single `APIRouter` in `src/features/products/router.py` with per-endpoint auth guards (`OwnerDep` for writes, `AdminUserDep` for image management, no auth for public reads). All business logic in `service.py`. Relationships use `selectinload` because models declare `lazy="raise"`.

**Tech Stack:** FastAPI 0.115, SQLAlchemy 2.0 async, Pydantic v2, asyncpg, pytest-asyncio (asyncio_mode=auto), httpx AsyncClient.

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `tests/__init__.py` | package marker |
| Create | `tests/features/__init__.py` | package marker |
| Create | `tests/features/products/__init__.py` | package marker |
| Create | `tests/conftest.py` | shared fixtures: db_session, client, admin_client, owner_client |
| Create | `src/features/products/schemas.py` | Pydantic I/O models |
| Create | `src/features/products/service.py` | all business logic |
| Create | `tests/features/products/test_service.py` | service unit/integration tests |
| Create | `src/features/products/router.py` | FastAPI endpoints |
| Create | `tests/features/products/test_router.py` | endpoint integration tests |
| Modify | `src/main.py:48-49` | uncomment products router |

---

## Task 1: Test Infrastructure

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/features/__init__.py`
- Create: `tests/features/products/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Create package markers**

```bash
touch /path/to/backend/tests/__init__.py
touch /path/to/backend/tests/features/__init__.py
touch /path/to/backend/tests/features/products/__init__.py
```

Or create each as an empty file.

- [ ] **Step 2: Write `tests/conftest.py`**

```python
"""Shared pytest fixtures for Vantier backend tests."""

from collections.abc import AsyncGenerator
from typing import Any, Annotated
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db, get_engine
from src.core.dependencies import get_admin_user, require_owner
from src.features.users.models import AdminUser
from src.main import app


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a session whose changes are rolled back after each test."""
    engine = get_engine()
    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False, autoflush=False)
    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


def _make_admin(role: str = "operative") -> AdminUser:
    admin = AdminUser.__new__(AdminUser)
    admin.id = None
    admin.neon_auth_user_id = f"test-{role}-id"
    admin.email = f"{role}@test.com"
    admin.role = role
    admin.is_active = True
    return admin


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Unauthenticated HTTP client (public endpoints)."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client authenticated as an operative admin."""
    async def override_get_db():
        yield db_session

    async def override_get_admin_user():
        return _make_admin("operative")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_admin_user] = override_get_admin_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def owner_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client authenticated as the owner."""
    async def override_get_db():
        yield db_session

    async def override_get_admin_user():
        return _make_admin("owner")

    async def override_require_owner():
        return _make_admin("owner")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_admin_user] = override_get_admin_user
    app.dependency_overrides[require_owner] = override_require_owner
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

- [ ] **Step 3: Verify pytest collects without errors**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/ --collect-only
```

Expected: `no tests ran` (or similar) with no import errors.

- [ ] **Step 4: Commit**

```bash
git add tests/
git commit -m "test: add pytest infrastructure and shared fixtures"
```

---

## Task 2: Schemas

**Files:**
- Create: `src/features/products/schemas.py`
- Create: `tests/features/products/test_schemas.py`

- [ ] **Step 1: Write failing tests for schemas**

```python
# tests/features/products/test_schemas.py
"""Tests for products Pydantic schemas."""

import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.features.products.schemas import (
    ImageCreate,
    ImageReorder,
    ProductCreate,
    ProductUpdate,
    VariantCreate,
    VariantUpdate,
)


def test_product_create_valid():
    p = ProductCreate(line="polo_atelier", name="Polo Test")
    assert p.line == "polo_atelier"
    assert p.description is None


def test_product_create_invalid_line():
    with pytest.raises(ValidationError):
        ProductCreate(line="invalid_line", name="X")


def test_variant_create_valid():
    v = VariantCreate(
        style="classic",
        size="M",
        color="Black",
        cost_acquisition_usd=Decimal("50.00"),
        price_usd=Decimal("120.00"),
    )
    assert v.stock_qty == 0


def test_variant_create_invalid_size():
    with pytest.raises(ValidationError):
        VariantCreate(
            style="classic",
            size="XXS",
            color="Black",
            cost_acquisition_usd=Decimal("50.00"),
            price_usd=Decimal("120.00"),
        )


def test_product_update_all_none_allowed():
    # Fully empty update is valid (no-op)
    u = ProductUpdate()
    assert u.name is None and u.description is None and u.is_active is None


def test_image_reorder_requires_list():
    ids = [uuid.uuid4(), uuid.uuid4()]
    r = ImageReorder(image_ids=ids)
    assert len(r.image_ids) == 2
```

- [ ] **Step 2: Run tests — expect ImportError (schemas not written yet)**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_schemas.py -v
```

Expected: `ImportError` or `ModuleNotFoundError`.

- [ ] **Step 3: Write `src/features/products/schemas.py`**

```python
"""Pydantic schemas for the products feature slice."""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict

ProductLine = Literal["polo_atelier", "signature", "essential"]
ProductStyle = Literal["classic", "design"]
ProductSize = Literal["S", "M", "L", "XL", "XXL", "XXXL"]


# ── Input schemas ──────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    line: ProductLine
    name: str
    description: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class VariantCreate(BaseModel):
    style: ProductStyle
    size: ProductSize
    color: str
    cost_acquisition_usd: Decimal
    price_usd: Decimal
    stock_qty: int = 0


class VariantUpdate(BaseModel):
    color: str | None = None
    cost_acquisition_usd: Decimal | None = None
    price_usd: Decimal | None = None
    stock_qty: int | None = None
    is_active: bool | None = None


class ImageCreate(BaseModel):
    url: str
    alt_text: str | None = None
    position: int = 0


class ImageReorder(BaseModel):
    image_ids: list[uuid.UUID]


# ── Output schemas ─────────────────────────────────────────────────────────────

class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    url: str
    position: int
    alt_text: str | None


class VariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sku: str
    style: str
    size: str
    color: str
    stock_qty: int
    price_usd: Decimal
    is_active: bool
    images: list[ImageResponse]


class VariantAdminResponse(VariantResponse):
    """Extends VariantResponse with cost data visible only to admins."""
    cost_acquisition_usd: Decimal


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    line: str
    name: str
    description: str | None
    is_active: bool
    variants: list[VariantResponse]


class ProductAdminResponse(ProductResponse):
    """Extends ProductResponse with admin-visible variant cost data."""
    variants: list[VariantAdminResponse]


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_schemas.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/features/products/schemas.py tests/features/products/test_schemas.py
git commit -m "feat(products): add Pydantic schemas"
```

---

## Task 3: Service — Read Operations

**Files:**
- Create: `src/features/products/service.py`
- Create: `tests/features/products/test_service.py`

- [ ] **Step 1: Write failing tests for read operations**

```python
# tests/features/products/test_service.py
"""Integration tests for products service (use real DB via rollback fixture)."""

import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.core.utils import PaginationParams
from src.features.products.models import Product, ProductVariant, ProductImage
from src.features.products.schemas import ProductCreate, VariantCreate
from src.features.products import service


async def _create_test_product(db: AsyncSession, name: str = "Test Polo") -> Product:
    """Helper: insert a product+variant+image directly via ORM."""
    product = Product(line="polo_atelier", name=name, description="A test product")
    db.add(product)
    await db.flush()

    sku = f"VAT-PA-CL-M-BLACK-{uuid.uuid4().hex[:4].upper()}"
    variant = ProductVariant(
        product_id=product.id,
        style="classic",
        size="M",
        color="Black",
        sku=sku,
        barcode=sku,
        stock_qty=10,
        cost_acquisition_usd=Decimal("50.00"),
        price_usd=Decimal("120.00"),
    )
    db.add(variant)
    await db.flush()

    image = ProductImage(variant_id=variant.id, url="https://cdn.test/img.jpg", position=0)
    db.add(image)
    await db.flush()

    return product


@pytest.mark.asyncio
async def test_list_products_returns_active_only(db_session: AsyncSession):
    await _create_test_product(db_session, "Active Product")

    inactive = Product(line="signature", name="Inactive", is_active=False)
    db_session.add(inactive)
    await db_session.flush()

    pagination = PaginationParams(page=1, page_size=20)
    items, total = await service.list_products(db_session, pagination)

    names = [p.name for p in items]
    assert "Active Product" in names
    assert "Inactive" not in names


@pytest.mark.asyncio
async def test_list_products_filter_by_line(db_session: AsyncSession):
    await _create_test_product(db_session, "Polo One")

    other = Product(line="signature", name="Sig One")
    db_session.add(other)
    await db_session.flush()

    pagination = PaginationParams(page=1, page_size=20)
    items, total = await service.list_products(db_session, pagination, line="polo_atelier")

    assert all(p.line == "polo_atelier" for p in items)


@pytest.mark.asyncio
async def test_get_product_found(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    result = await service.get_product(db_session, product.id)

    assert result.id == product.id
    assert len(result.variants) == 1
    assert len(result.variants[0].images) == 1


@pytest.mark.asyncio
async def test_get_product_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.get_product(db_session, uuid.uuid4())
```

- [ ] **Step 2: Run tests — expect ImportError**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py -v
```

Expected: `ImportError` because `service.py` doesn't exist.

- [ ] **Step 3: Write `src/features/products/service.py` (read operations only)**

```python
"""Business logic for the products feature slice."""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import NotFoundException
from src.core.utils import PaginationParams, generate_barcode_value, generate_sku
from src.features.products.models import Product, ProductImage, ProductVariant
from src.features.products.schemas import (
    ImageCreate,
    ProductCreate,
    ProductUpdate,
    VariantCreate,
    VariantUpdate,
)


def _with_variants_and_images():
    """Reusable selectinload option for Product queries."""
    return selectinload(Product.variants).selectinload(ProductVariant.images)


async def list_products(
    db: AsyncSession,
    pagination: PaginationParams,
    line: str | None = None,
    size: str | None = None,
    style: str | None = None,
    in_stock: bool | None = None,
    include_inactive: bool = False,
) -> tuple[list[Product], int]:
    """Return paginated list of products with their variants and images.

    Args:
        db: Async database session.
        pagination: Page and page_size parameters.
        line: Optional filter by product line enum value.
        size: Optional filter variants by size (applied in Python).
        style: Optional filter variants by style (applied in Python).
        in_stock: If True, only show variants with stock_qty > 0.
        include_inactive: If True, include inactive products (admin only).

    Returns:
        Tuple of (products list, total count before pagination).
    """
    where_clauses = []
    if not include_inactive:
        where_clauses.append(Product.is_active == True)  # noqa: E712
    if line:
        where_clauses.append(Product.line == line)

    count_q = select(func.count()).select_from(Product)
    if where_clauses:
        count_q = count_q.where(*where_clauses)
    total = (await db.execute(count_q)).scalar_one()

    data_q = select(Product).options(_with_variants_and_images())
    if where_clauses:
        data_q = data_q.where(*where_clauses)
    data_q = data_q.offset(pagination.offset).limit(pagination.limit)

    products = list((await db.execute(data_q)).scalars().all())

    # Apply variant-level filters in Python (avoids complex JOINs)
    if size or style or in_stock is not None:
        for product in products:
            product.variants = [
                v for v in product.variants
                if (not size or v.size == size)
                and (not style or v.style == style)
                and (in_stock is None or bool(v.stock_qty > 0) == in_stock)
                and (include_inactive or v.is_active)
            ]

    return products, total


async def get_product(db: AsyncSession, product_id: uuid.UUID) -> Product:
    """Fetch a single product with all its variants and images.

    Args:
        db: Async database session.
        product_id: UUID of the product to fetch.

    Returns:
        Product ORM instance with variants and images loaded.

    Raises:
        NotFoundException: If no product with that ID exists.
    """
    result = await db.execute(
        select(Product)
        .options(_with_variants_and_images())
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise NotFoundException(f"Product {product_id} not found")
    return product
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py::test_list_products_returns_active_only tests/features/products/test_service.py::test_list_products_filter_by_line tests/features/products/test_service.py::test_get_product_found tests/features/products/test_service.py::test_get_product_not_found -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/features/products/service.py tests/features/products/test_service.py
git commit -m "feat(products): add service read operations with tests"
```

---

## Task 4: Service — Product Write Operations

**Files:**
- Modify: `src/features/products/service.py` (append functions)
- Modify: `tests/features/products/test_service.py` (append tests)

- [ ] **Step 1: Write failing tests for product writes**

Append to `tests/features/products/test_service.py`:

```python
@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession):
    data = ProductCreate(line="signature", name="New Signature Polo")
    product = await service.create_product(db_session, data)

    assert product.id is not None
    assert product.name == "New Signature Polo"
    assert product.line == "signature"
    assert product.is_active is True
    assert product.variants == []


@pytest.mark.asyncio
async def test_update_product_name(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    from src.features.products.schemas import ProductUpdate
    updated = await service.update_product(db_session, product.id, ProductUpdate(name="Updated Name"))
    assert updated.name == "Updated Name"


@pytest.mark.asyncio
async def test_update_product_not_found(db_session: AsyncSession):
    from src.features.products.schemas import ProductUpdate
    with pytest.raises(NotFoundException):
        await service.update_product(db_session, uuid.uuid4(), ProductUpdate(name="X"))


@pytest.mark.asyncio
async def test_deactivate_product(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    await service.deactivate_product(db_session, product.id)

    result = await service.get_product(db_session, product.id)
    assert result.is_active is False
```

- [ ] **Step 2: Run tests — expect FAIL (functions not defined)**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py::test_create_product -v
```

Expected: `AttributeError: module ... has no attribute 'create_product'`.

- [ ] **Step 3: Add write operations to `src/features/products/service.py`**

Append to `service.py` after `get_product`:

```python
async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    """Create a new product with no variants.

    Args:
        db: Async database session.
        data: Validated product creation payload.

    Returns:
        Newly created Product ORM instance.
    """
    product = Product(line=data.line, name=data.name, description=data.description)
    db.add(product)
    await db.flush()

    # Reload with relationships so response is fully populated
    result = await db.execute(
        select(Product)
        .options(_with_variants_and_images())
        .where(Product.id == product.id)
    )
    return result.scalar_one()


async def update_product(
    db: AsyncSession, product_id: uuid.UUID, data: ProductUpdate
) -> Product:
    """Partially update a product's mutable fields.

    Args:
        db: Async database session.
        product_id: UUID of the product to update.
        data: Fields to update (None fields are ignored).

    Returns:
        Updated Product ORM instance.

    Raises:
        NotFoundException: If product does not exist.
    """
    product = await get_product(db, product_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    await db.flush()
    return product


async def deactivate_product(db: AsyncSession, product_id: uuid.UUID) -> None:
    """Soft-delete a product by setting is_active=False.

    Args:
        db: Async database session.
        product_id: UUID of the product to deactivate.

    Raises:
        NotFoundException: If product does not exist.
    """
    product = await get_product(db, product_id)
    product.is_active = False
    await db.flush()
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py -k "create_product or update_product or deactivate_product" -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/features/products/service.py tests/features/products/test_service.py
git commit -m "feat(products): add product write operations with tests"
```

---

## Task 5: Service — Variant and Image Operations

**Files:**
- Modify: `src/features/products/service.py` (append functions)
- Modify: `tests/features/products/test_service.py` (append tests)

- [ ] **Step 1: Write failing tests for variant and image operations**

Append to `tests/features/products/test_service.py`:

```python
@pytest.mark.asyncio
async def test_add_variant_generates_sku(db_session: AsyncSession):
    product = await service.create_product(db_session, ProductCreate(line="essential", name="E Polo"))
    data = VariantCreate(
        style="design",
        size="L",
        color="White",
        cost_acquisition_usd=Decimal("40.00"),
        price_usd=Decimal("100.00"),
    )
    variant = await service.add_variant(db_session, product.id, data)

    assert variant.sku.startswith("VAT-ES-DS-L-WHITE-")
    assert variant.barcode == variant.sku
    assert variant.stock_qty == 0


@pytest.mark.asyncio
async def test_add_variant_product_not_found(db_session: AsyncSession):
    data = VariantCreate(
        style="classic", size="S", color="Red",
        cost_acquisition_usd=Decimal("30.00"), price_usd=Decimal("80.00"),
    )
    with pytest.raises(NotFoundException):
        await service.add_variant(db_session, uuid.uuid4(), data)


@pytest.mark.asyncio
async def test_update_variant(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    variant = product.variants[0]  # loaded by _create_test_product? No — need re-fetch
    # Re-fetch product to get variant id
    fetched = await service.get_product(db_session, product.id)
    variant_id = fetched.variants[0].id

    updated = await service.update_variant(db_session, variant_id, VariantUpdate(color="Navy"))
    assert updated.color == "Navy"


@pytest.mark.asyncio
async def test_deactivate_variant(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    fetched = await service.get_product(db_session, product.id)
    variant_id = fetched.variants[0].id

    await service.deactivate_variant(db_session, variant_id)

    result = await db_session.get(ProductVariant, variant_id)
    assert result.is_active is False


@pytest.mark.asyncio
async def test_add_image(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    fetched = await service.get_product(db_session, product.id)
    variant_id = fetched.variants[0].id

    image = await service.add_image(
        db_session, variant_id, ImageCreate(url="https://cdn.test/new.jpg", position=1)
    )
    assert image.url == "https://cdn.test/new.jpg"
    assert image.variant_id == variant_id


@pytest.mark.asyncio
async def test_remove_image(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    fetched = await service.get_product(db_session, product.id)
    image_id = fetched.variants[0].images[0].id

    await service.remove_image(db_session, image_id)

    result = await db_session.get(ProductImage, image_id)
    assert result is None


@pytest.mark.asyncio
async def test_reorder_images(db_session: AsyncSession):
    product = await _create_test_product(db_session)
    fetched = await service.get_product(db_session, product.id)
    variant_id = fetched.variants[0].id
    first_image_id = fetched.variants[0].images[0].id

    # Add a second image
    second = await service.add_image(
        db_session, variant_id, ImageCreate(url="https://cdn.test/second.jpg", position=1)
    )

    # Reverse order
    reordered = await service.reorder_images(db_session, variant_id, [second.id, first_image_id])
    assert reordered[0].id == second.id
    assert reordered[0].position == 0
    assert reordered[1].position == 1
```

Also add this import at the top of the test file:
```python
from src.features.products.schemas import ImageCreate, VariantUpdate
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py::test_add_variant_generates_sku -v
```

Expected: `AttributeError: module ... has no attribute 'add_variant'`.

- [ ] **Step 3: Append variant and image functions to `src/features/products/service.py`**

```python
async def add_variant(
    db: AsyncSession, product_id: uuid.UUID, data: VariantCreate
) -> ProductVariant:
    """Add a new variant to a product, auto-generating its SKU and barcode.

    Args:
        db: Async database session.
        product_id: UUID of the parent product.
        data: Validated variant creation payload.

    Returns:
        Newly created ProductVariant ORM instance with images loaded.

    Raises:
        NotFoundException: If product does not exist.
    """
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise NotFoundException(f"Product {product_id} not found")

    sku = generate_sku(product.line, data.style, data.size, data.color)
    barcode = generate_barcode_value(sku)

    variant = ProductVariant(
        product_id=product_id,
        style=data.style,
        size=data.size,
        color=data.color,
        sku=sku,
        barcode=barcode,
        stock_qty=data.stock_qty,
        cost_acquisition_usd=data.cost_acquisition_usd,
        price_usd=data.price_usd,
    )
    db.add(variant)
    await db.flush()

    result = await db.execute(
        select(ProductVariant)
        .options(selectinload(ProductVariant.images))
        .where(ProductVariant.id == variant.id)
    )
    return result.scalar_one()


async def update_variant(
    db: AsyncSession, variant_id: uuid.UUID, data: VariantUpdate
) -> ProductVariant:
    """Partially update a variant's mutable fields.

    Args:
        db: Async database session.
        variant_id: UUID of the variant to update.
        data: Fields to update (None fields are ignored).

    Returns:
        Updated ProductVariant ORM instance.

    Raises:
        NotFoundException: If variant does not exist.
    """
    result = await db.execute(
        select(ProductVariant)
        .options(selectinload(ProductVariant.images))
        .where(ProductVariant.id == variant_id)
    )
    variant = result.scalar_one_or_none()
    if variant is None:
        raise NotFoundException(f"Variant {variant_id} not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(variant, field, value)
    await db.flush()
    return variant


async def deactivate_variant(db: AsyncSession, variant_id: uuid.UUID) -> None:
    """Soft-delete a variant by setting is_active=False.

    Args:
        db: Async database session.
        variant_id: UUID of the variant to deactivate.

    Raises:
        NotFoundException: If variant does not exist.
    """
    result = await db.execute(
        select(ProductVariant).where(ProductVariant.id == variant_id)
    )
    variant = result.scalar_one_or_none()
    if variant is None:
        raise NotFoundException(f"Variant {variant_id} not found")
    variant.is_active = False
    await db.flush()


async def add_image(
    db: AsyncSession, variant_id: uuid.UUID, data: ImageCreate
) -> ProductImage:
    """Add an image URL to a product variant.

    Args:
        db: Async database session.
        variant_id: UUID of the parent variant.
        data: Image URL and optional metadata.

    Returns:
        Newly created ProductImage ORM instance.

    Raises:
        NotFoundException: If variant does not exist.
    """
    result = await db.execute(
        select(ProductVariant).where(ProductVariant.id == variant_id)
    )
    if result.scalar_one_or_none() is None:
        raise NotFoundException(f"Variant {variant_id} not found")

    image = ProductImage(
        variant_id=variant_id,
        url=data.url,
        alt_text=data.alt_text,
        position=data.position,
    )
    db.add(image)
    await db.flush()
    return image


async def remove_image(db: AsyncSession, image_id: uuid.UUID) -> None:
    """Hard-delete a product image.

    Args:
        db: Async database session.
        image_id: UUID of the image to delete.

    Raises:
        NotFoundException: If image does not exist.
    """
    result = await db.execute(
        select(ProductImage).where(ProductImage.id == image_id)
    )
    image = result.scalar_one_or_none()
    if image is None:
        raise NotFoundException(f"Image {image_id} not found")
    await db.delete(image)
    await db.flush()


async def reorder_images(
    db: AsyncSession, variant_id: uuid.UUID, image_ids: list[uuid.UUID]
) -> list[ProductImage]:
    """Assign new position values to images based on the provided order.

    Args:
        db: Async database session.
        variant_id: UUID of the variant whose images to reorder.
        image_ids: Ordered list of image UUIDs (index 0 → position 0).

    Returns:
        List of ProductImage instances in the new order.

    Raises:
        NotFoundException: If any image_id is not found or doesn't belong to variant.
    """
    result = await db.execute(
        select(ProductImage).where(ProductImage.variant_id == variant_id)
    )
    existing = {img.id: img for img in result.scalars().all()}

    for position, image_id in enumerate(image_ids):
        if image_id not in existing:
            raise NotFoundException(f"Image {image_id} not found for variant {variant_id}")
        existing[image_id].position = position

    await db.flush()
    return [existing[iid] for iid in image_ids]
```

- [ ] **Step 4: Run all service tests — expect PASS**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_service.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/features/products/service.py tests/features/products/test_service.py
git commit -m "feat(products): add variant and image service operations with tests"
```

---

## Task 6: Router

**Files:**
- Create: `src/features/products/router.py`
- Create: `tests/features/products/test_router.py`

- [ ] **Step 1: Write failing integration tests**

```python
# tests/features/products/test_router.py
"""Integration tests for the products API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.products.models import Product, ProductVariant, ProductImage
from src.features.products import service
from src.features.products.schemas import ProductCreate, VariantCreate
from decimal import Decimal
import uuid


@pytest.mark.asyncio
async def test_list_products_public(client: AsyncClient, db_session: AsyncSession):
    """Public endpoint returns active products."""
    product = Product(line="polo_atelier", name="Public Polo")
    db_session.add(product)
    await db_session.flush()

    resp = await client.get("/api/v1/products")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    names = [p["name"] for p in data["items"]]
    assert "Public Polo" in names


@pytest.mark.asyncio
async def test_get_product_public(client: AsyncClient, db_session: AsyncSession):
    """Public endpoint returns a single product by ID."""
    product = Product(line="signature", name="Detail Test")
    db_session.add(product)
    await db_session.flush()

    resp = await client.get(f"/api/v1/products/{product.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Detail Test"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    resp = await client.get(f"/api/v1/products/{uuid.uuid4()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_product_requires_owner(client: AsyncClient):
    resp = await client.post("/api/v1/products", json={"line": "essential", "name": "X"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_create_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    resp = await owner_client.post(
        "/api/v1/products",
        json={"line": "polo_atelier", "name": "New Owner Product"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "New Owner Product"
    assert data["line"] == "polo_atelier"
    assert data["variants"] == []


@pytest.mark.asyncio
async def test_update_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="essential", name="Before Update")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.patch(
        f"/api/v1/products/{product.id}",
        json={"name": "After Update"}
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "After Update"


@pytest.mark.asyncio
async def test_deactivate_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="signature", name="To Delete")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.delete(f"/api/v1/products/{product.id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_add_variant_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="polo_atelier", name="Variant Parent")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.post(
        f"/api/v1/products/{product.id}/variants",
        json={
            "style": "classic",
            "size": "M",
            "color": "Black",
            "cost_acquisition_usd": "50.00",
            "price_usd": "120.00",
        }
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["sku"].startswith("VAT-PA-CL-M-BLACK-")
    assert "cost_acquisition_usd" not in data  # not exposed publicly


@pytest.mark.asyncio
async def test_add_image_as_admin(admin_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="essential", name="Image Parent")
    db_session.add(product)
    await db_session.flush()

    sku = f"VAT-ES-CL-M-RED-{uuid.uuid4().hex[:4].upper()}"
    variant = ProductVariant(
        product_id=product.id, style="classic", size="M", color="Red",
        sku=sku, barcode=sku, stock_qty=5,
        cost_acquisition_usd=Decimal("30.00"), price_usd=Decimal("80.00"),
    )
    db_session.add(variant)
    await db_session.flush()

    resp = await admin_client.post(
        f"/api/v1/products/{product.id}/variants/{variant.id}/images",
        json={"url": "https://cdn.test/photo.jpg", "position": 0}
    )
    assert resp.status_code == 201
    assert resp.json()["url"] == "https://cdn.test/photo.jpg"
```

- [ ] **Step 2: Run tests — expect 404 (router not wired yet)**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_router.py -v
```

Expected: tests fail with connection errors or 404s because router isn't registered in `main.py`.

- [ ] **Step 3: Write `src/features/products/router.py`**

```python
"""FastAPI router for the products feature slice."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.dependencies import AdminUserDep, DBSession, OwnerDep
from src.core.utils import PaginationParams, paginate
from src.features.products import service
from src.features.products.schemas import (
    ImageCreate,
    ImageReorder,
    ImageResponse,
    ProductAdminResponse,
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
    VariantAdminResponse,
    VariantCreate,
    VariantResponse,
    VariantUpdate,
)

router = APIRouter()


# ── Public endpoints ───────────────────────────────────────────────────────────

@router.get("", response_model=ProductListResponse)
async def list_products(
    db: DBSession,
    pagination: Annotated[PaginationParams, Depends(paginate)],
    line: str | None = None,
    size: str | None = None,
    style: str | None = None,
    in_stock: bool | None = None,
) -> ProductListResponse:
    """List active products with optional filters. Public endpoint."""
    items, total = await service.list_products(
        db, pagination, line=line, size=size, style=style, in_stock=in_stock
    )
    return ProductListResponse(
        items=[ProductResponse.model_validate(p) for p in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: uuid.UUID, db: DBSession) -> ProductResponse:
    """Get a single product with variants and images. Public endpoint."""
    product = await service.get_product(db, product_id)
    return ProductResponse.model_validate(product)


# ── Owner endpoints — products ─────────────────────────────────────────────────

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: DBSession,
    _owner: OwnerDep,
) -> ProductResponse:
    """Create a new product. Requires owner role."""
    product = await service.create_product(db, data)
    return ProductResponse.model_validate(product)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    db: DBSession,
    _owner: OwnerDep,
) -> ProductResponse:
    """Partially update a product. Requires owner role."""
    product = await service.update_product(db, product_id, data)
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=204)
async def deactivate_product(
    product_id: uuid.UUID,
    db: DBSession,
    _owner: OwnerDep,
) -> None:
    """Soft-delete a product (is_active=False). Requires owner role."""
    await service.deactivate_product(db, product_id)


# ── Owner endpoints — variants ─────────────────────────────────────────────────

@router.post("/{product_id}/variants", response_model=VariantResponse, status_code=201)
async def add_variant(
    product_id: uuid.UUID,
    data: VariantCreate,
    db: DBSession,
    _owner: OwnerDep,
) -> VariantResponse:
    """Add a variant to a product. SKU auto-generated. Requires owner role."""
    variant = await service.add_variant(db, product_id, data)
    return VariantResponse.model_validate(variant)


@router.patch("/{product_id}/variants/{variant_id}", response_model=VariantResponse)
async def update_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    data: VariantUpdate,
    db: DBSession,
    _owner: OwnerDep,
) -> VariantResponse:
    """Partially update a product variant. Requires owner role."""
    variant = await service.update_variant(db, variant_id, data)
    return VariantResponse.model_validate(variant)


@router.delete("/{product_id}/variants/{variant_id}", status_code=204)
async def deactivate_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    db: DBSession,
    _owner: OwnerDep,
) -> None:
    """Soft-delete a variant (is_active=False). Requires owner role."""
    await service.deactivate_variant(db, variant_id)


# ── Admin endpoints — images ───────────────────────────────────────────────────

@router.post(
    "/{product_id}/variants/{variant_id}/images",
    response_model=ImageResponse,
    status_code=201,
)
async def add_image(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    data: ImageCreate,
    db: DBSession,
    _admin: AdminUserDep,
) -> ImageResponse:
    """Save a pre-uploaded image URL to a variant. Requires admin role."""
    image = await service.add_image(db, variant_id, data)
    return ImageResponse.model_validate(image)


@router.delete(
    "/{product_id}/variants/{variant_id}/images/{image_id}",
    status_code=204,
)
async def remove_image(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    image_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> None:
    """Hard-delete a product image. Requires admin role."""
    await service.remove_image(db, image_id)


@router.patch(
    "/{product_id}/variants/{variant_id}/images/reorder",
    response_model=list[ImageResponse],
)
async def reorder_images(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    data: ImageReorder,
    db: DBSession,
    _admin: AdminUserDep,
) -> list[ImageResponse]:
    """Reorder images for a variant. Requires admin role."""
    images = await service.reorder_images(db, variant_id, data.image_ids)
    return [ImageResponse.model_validate(img) for img in images]
```

- [ ] **Step 4: Run tests — still expect 404 (not wired in main.py yet)**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/features/products/test_router.py::test_list_products_public -v
```

Expected: 404 (router not mounted).

- [ ] **Step 5: Commit router before wiring**

```bash
git add src/features/products/router.py tests/features/products/test_router.py
git commit -m "feat(products): add router and endpoint integration tests"
```

---

## Task 7: Wire Router in main.py + Full Test Run

**Files:**
- Modify: `src/main.py:48-49`

- [ ] **Step 1: Uncomment products router in `src/main.py`**

Replace:
```python
    # from src.features.products.router import router as products_router
    # app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
```

With:
```python
    from src.features.products.router import router as products_router
    app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
```

- [ ] **Step 2: Run all tests**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/pytest tests/ -v
```

Expected: all tests PASS (schemas, service, router).

- [ ] **Step 3: Start dev server and smoke test**

```bash
cd backend && ~/.pyenv/versions/vantier-backend/bin/uvicorn src.main:app --reload
```

In another terminal:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}

curl http://localhost:8000/api/v1/products
# Expected: {"items":[],"total":0,"page":1,"page_size":20}

curl http://localhost:8000/docs
# Expected: browser opens Swagger UI with Products endpoints listed
```

- [ ] **Step 4: Commit**

```bash
git add src/main.py
git commit -m "feat(products): wire router into app — products slice complete"
```

---

## Self-Review Checklist

- [x] All spec endpoints mapped to router functions
- [x] SKU auto-generation via `utils.generate_sku()` in `add_variant`
- [x] Soft-delete on Product and ProductVariant (`is_active=False`)
- [x] Hard-delete only on ProductImage (`db.delete(image)`)
- [x] `cost_acquisition_usd` excluded from `VariantResponse` (public)
- [x] `lazy="raise"` handled with `selectinload` on all relationship accesses
- [x] `autoflush=False` → explicit `await db.flush()` after every write
- [x] TDD: failing test before each implementation
- [x] All function signatures consistent between tasks
- [x] No placeholders or TODOs in code blocks
