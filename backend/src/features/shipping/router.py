"""Shipping feature router — exposes rate lookup for the checkout flow."""

from __future__ import annotations

from fastapi import APIRouter, Query

from src.features.shipping.schemas import FreeShippingResponse, ShippingRateResponse
from src.integrations import envia_client

router = APIRouter()

_WAREHOUSE_ZIP = "20000"   # Aguascalientes
_FREE_SHIPPING_THRESHOLD = 5


@router.get(
    "/rates",
    response_model=list[ShippingRateResponse],
    summary="Get available shipping rates for a destination ZIP code",
)
async def get_shipping_rates(
    zip: str = Query(..., description="Customer destination ZIP / postal code"),
    country: str = Query("US", description="Customer destination country code"),
    item_count: int = Query(..., ge=1, description="Total number of items in the cart"),
) -> list[ShippingRateResponse]:
    """Return carrier options and prices for the given destination.

    When item_count >= 5, a single free shipping option is returned.
    Otherwise, rates are fetched live from envia.com (with a mock fallback
    when the API key is not configured).
    """
    if item_count >= _FREE_SHIPPING_THRESHOLD:
        free = FreeShippingResponse()
        return [ShippingRateResponse(**free.model_dump())]

    raw_rates = await envia_client.get_shipping_rates(
        origin_zip=_WAREHOUSE_ZIP,
        destination_zip=zip,
        destination_country=country,
    )
    return [ShippingRateResponse(**r) for r in raw_rates]
