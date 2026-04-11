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


async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    """Create a new product with no variants.

    Args:
        db: Async database session.
        data: Validated product creation payload.

    Returns:
        Newly created Product ORM instance with variants loaded (empty list).
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
        Updated ProductVariant ORM instance with images loaded.

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
        NotFoundException: If any image_id does not belong to this variant.
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
