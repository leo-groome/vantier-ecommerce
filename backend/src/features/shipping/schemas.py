"""Pydantic schemas for the shipping feature slice."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ShippingRateResponse(BaseModel):
    """A single shipping option returned to the frontend for carrier selection."""

    carrier_id: str
    carrier_name: str
    service: str
    price_usd: float
    estimated_days: int


class FreeShippingResponse(BaseModel):
    """Returned when the order qualifies for free shipping (5+ items)."""

    carrier_id: str = "free"
    carrier_name: str = "Standard Shipping"
    service: str = "Free"
    price_usd: float = Field(default=0.0)
    estimated_days: int = 7
