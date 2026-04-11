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
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
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
