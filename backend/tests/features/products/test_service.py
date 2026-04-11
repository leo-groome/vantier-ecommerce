"""Integration tests for products service (rollback fixture ensures DB isolation)."""

import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.core.utils import PaginationParams
from src.features.products.models import Product, ProductImage, ProductVariant
from src.features.products import service


async def _create_test_product(db: AsyncSession, name: str = "Test Polo") -> Product:
    """Helper: insert a product+variant+image via ORM."""
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
    items, _ = await service.list_products(db_session, pagination, line="polo_atelier")

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


# ── Product write tests ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession):
    from src.features.products.schemas import ProductCreate
    data = ProductCreate(line="signature", name="New Signature Polo")
    product = await service.create_product(db_session, data)

    assert product.id is not None
    assert product.name == "New Signature Polo"
    assert product.line == "signature"
    assert product.is_active is True
    assert product.variants == []


@pytest.mark.asyncio
async def test_update_product_name(db_session: AsyncSession):
    from src.features.products.schemas import ProductUpdate
    product = await _create_test_product(db_session)
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


# ── Variant and image tests ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_add_variant_generates_sku(db_session: AsyncSession):
    from src.features.products.schemas import ProductCreate, VariantCreate
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
    from src.features.products.schemas import VariantCreate
    data = VariantCreate(
        style="classic", size="S", color="Red",
        cost_acquisition_usd=Decimal("30.00"), price_usd=Decimal("80.00"),
    )
    with pytest.raises(NotFoundException):
        await service.add_variant(db_session, uuid.uuid4(), data)


@pytest.mark.asyncio
async def test_update_variant(db_session: AsyncSession):
    from src.features.products.schemas import VariantUpdate
    product = await _create_test_product(db_session)
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

    from sqlalchemy import select as sa_select
    from src.features.products.models import ProductVariant as PV
    result = await db_session.execute(sa_select(PV).where(PV.id == variant_id))
    assert result.scalar_one().is_active is False


@pytest.mark.asyncio
async def test_add_image(db_session: AsyncSession):
    from src.features.products.schemas import ImageCreate
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

    from sqlalchemy import select as sa_select
    from src.features.products.models import ProductImage as PI
    result = await db_session.execute(sa_select(PI).where(PI.id == image_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_reorder_images(db_session: AsyncSession):
    from src.features.products.schemas import ImageCreate
    product = await _create_test_product(db_session)
    fetched = await service.get_product(db_session, product.id)
    variant_id = fetched.variants[0].id
    first_image_id = fetched.variants[0].images[0].id

    second = await service.add_image(
        db_session, variant_id, ImageCreate(url="https://cdn.test/second.jpg", position=1)
    )

    reordered = await service.reorder_images(db_session, variant_id, [second.id, first_image_id])
    assert reordered[0].id == second.id
    assert reordered[0].position == 0
    assert reordered[1].position == 1
