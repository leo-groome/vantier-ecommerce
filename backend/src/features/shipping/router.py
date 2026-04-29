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
    city: str = Query("", description="Customer city (improves rate accuracy)"),
    state: str = Query("", description="Customer state/province code"),
    district: str = Query("", description="Customer neighborhood/colonia (required for Paquetexpress in MX)"),
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
        destination_city=city,
        destination_state=state,
        destination_district=district,
    )
    return [ShippingRateResponse(**r) for r in raw_rates]
