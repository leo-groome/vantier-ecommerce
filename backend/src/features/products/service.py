"""Business logic for the products feature slice."""

from __future__ import annotations

import uuid

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
