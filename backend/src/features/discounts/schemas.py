"""Pydantic schemas for the discounts feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DiscountType = Literal["percent", "fixed"]


# ── Input schemas ──────────────────────────────────────────────────────────────

class DiscountCodeCreate(BaseModel):
    """Create a new discount code."""

    code: str = Field(..., min_length=1, max_length=100)
    type: DiscountType
    value: Decimal = Field(..., gt=0)
    usage_limit: int | None = Field(None, gt=0)
    expires_at: datetime | None = None


class DiscountCodeUpdate(BaseModel):
    """Partial update for a discount code."""

    usage_limit: int | None = Field(None, gt=0)
    expires_at: datetime | None = None
    is_active: bool | None = None


class DiscountValidateRequest(BaseModel):
    """Request to validate a discount code against an order total."""

    code: str
    order_subtotal_usd: Decimal = Field(..., gt=0)


# ── Output schemas ─────────────────────────────────────────────────────────────

class DiscountCodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    type: str
    value: Decimal
    usage_limit: int | None
    usage_count: int
    expires_at: datetime | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DiscountValidateResponse(BaseModel):
    """Result of validating a discount code."""

    code: str
    type: str
    value: Decimal
    discount_amount_usd: Decimal = Field(
        ..., description="Computed discount to apply to the order subtotal"
    )
    new_total_usd: Decimal = Field(..., description="Subtotal after discount applied")
    margin_warning: bool = Field(
        default=False,
        description="True when the discounted margin would be below 50% "
                    "(informational — not blocked at this layer; checkout enforces it)",
    )
