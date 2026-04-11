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
