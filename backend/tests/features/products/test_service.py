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
