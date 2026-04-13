"""Pydantic schemas for the inventory feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ── Input schemas ──────────────────────────────────────────────────────────────

class StockAdjustment(BaseModel):
    """Payload for adjusting a variant's stock quantity."""

    delta: int = Field(..., description="Units to add (positive) or remove (negative)")
    reason: str | None = Field(None, max_length=500)


class OperatingCostCreate(BaseModel):
    """Create a new per-order operating cost entry."""

    label: str = Field(..., max_length=200)
    amount_usd: Decimal = Field(..., gt=0)
    is_recurring: bool = True
    notes: str | None = None


class OperatingCostUpdate(BaseModel):
    """Partial update for an operating cost entry."""

    label: str | None = Field(None, max_length=200)
    amount_usd: Decimal | None = Field(None, gt=0)
    is_recurring: bool | None = None
    notes: str | None = None


# ── Output schemas ─────────────────────────────────────────────────────────────

class StockAdjustmentResponse(BaseModel):
    """Result of a stock adjustment operation."""

    variant_id: uuid.UUID
    new_stock_qty: int
    low_stock_alert: bool = Field(
        ..., description="True when new_stock_qty <= low-stock threshold (50)"
    )


class OperatingCostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    label: str
    amount_usd: Decimal
    is_recurring: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime
