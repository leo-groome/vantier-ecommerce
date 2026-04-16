"""Pydantic schemas for the exchanges feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


ExchangeStatus = Literal["requested", "approved", "shipped", "completed", "rejected"]


# ── Input schemas ──────────────────────────────────────────────────────────────

class ExchangeCreate(BaseModel):
    """Customer creates an exchange request for a variant within an order."""

    order_id: uuid.UUID
    original_variant_id: uuid.UUID
    customer_notes: str | None = None


class ExchangeAdminUpdate(BaseModel):
    """Admin approves/rejects/ships an exchange, optionally assigning replacement."""

    status: ExchangeStatus | None = None
    replacement_variant_id: uuid.UUID | None = None
    admin_notes: str | None = None


# ── Output schemas ─────────────────────────────────────────────────────────────

class ExchangeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    original_variant_id: uuid.UUID
    replacement_variant_id: uuid.UUID | None
    status: str
    customer_notes: str | None
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime
