"""Pydantic schemas for the orders feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ── Input schemas ──────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    """A single line item in the order request."""

    variant_id: uuid.UUID
    qty: int = Field(..., gt=0)


class ShippingAddressCreate(BaseModel):
    """Destination shipping address for an order."""

    full_name: str = Field(..., min_length=1)
    line1: str = Field(..., min_length=1)
    line2: str | None = None
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zip: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    phone: str | None = None


class OrderCreate(BaseModel):
    """Request body for creating an order and initiating checkout."""

    customer_email: EmailStr
    customer_name: str = Field(..., min_length=1)
    items: list[OrderItemCreate] = Field(..., min_length=1)
    shipping_address: ShippingAddressCreate
    discount_code: str | None = None  # raw code string; resolved and validated in service
    # Shipping rate selected by the user on the checkout shipping step.
    # Sent by the frontend after calling GET /shipping/rates.
    selected_carrier_name: str = Field(default="Standard Shipping")
    shipping_usd: Decimal = Field(default=Decimal("9.99"), ge=0)


# ── Output schemas ─────────────────────────────────────────────────────────────

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    variant_id: uuid.UUID
    qty: int
    unit_price_usd: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    neon_auth_user_id: str | None
    customer_email: str
    customer_name: str | None
    status: str
    payment_status: str
    subtotal_usd: Decimal
    shipping_usd: Decimal
    discount_usd: Decimal
    total_usd: Decimal
    is_free_shipping: bool
    shipping_address: dict
    carrier_tracking_number: str | None
    envia_label_url: str | None
    discount_code_id: uuid.UUID | None
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime


class CheckoutResponse(BaseModel):
    """Response after creating an order and Stripe Checkout Session."""

    order_id: uuid.UUID
    checkout_url: str  # Stripe-hosted URL; stub returns a mock URL


class PaymentIntentResponse(BaseModel):
    """Response after creating an order with an embedded PaymentIntent."""

    order_id: uuid.UUID
    client_secret: str   # Passed to Stripe.js Payment Element on the frontend
    amount_cents: int


class OrderStatusUpdate(BaseModel):
    """Admin request to transition an order's status."""

    status: Literal["processing", "shipped", "delivered", "cancelled"]
