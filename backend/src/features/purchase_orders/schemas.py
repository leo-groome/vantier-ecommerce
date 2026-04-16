"""Pydantic schemas for the purchase_orders feature slice."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


POStatus = Literal["ordered", "in_transit", "received"]


# ── Input schemas ──────────────────────────────────────────────────────────────

class POItemCreate(BaseModel):
    """A single line item when creating a PO."""

    variant_id: uuid.UUID
    qty_ordered: int = Field(..., gt=0)


class PurchaseOrderCreate(BaseModel):
    """Create a new purchase order."""

    reference_number: str = Field(..., min_length=1, max_length=50)
    supplier_name: str = Field(..., min_length=1, max_length=200)
    expected_arrival_date: date | None = None
    notes: str | None = None
    items: list[POItemCreate] = Field(..., min_length=1)


class PurchaseOrderUpdate(BaseModel):
    """Partial update for a PO (before it's received)."""

    supplier_name: str | None = Field(None, min_length=1, max_length=200)
    expected_arrival_date: date | None = None
    notes: str | None = None


class POStatusUpdate(BaseModel):
    """Transition a PO to a new status."""

    status: POStatus


# ── Output schemas ─────────────────────────────────────────────────────────────

class POItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    po_id: uuid.UUID
    variant_id: uuid.UUID
    qty_ordered: int
    qty_received: int
    created_at: datetime


class PurchaseOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    reference_number: str
    supplier_name: str
    expected_arrival_date: date | None
    status: str
    notes: str | None
    created_by_user_id: uuid.UUID | None
    items: list[POItemResponse]
    created_at: datetime
    updated_at: datetime
