"""Envia.com integration — shipping rate lookup and label generation."""

from __future__ import annotations

import logging
from decimal import Decimal

import httpx

from src.core.config import get_settings
from src.core.exceptions import AppException

logger = logging.getLogger(__name__)

# Standard Vantier package dimensions (cm) and weight (kg)
_PACKAGE = {
    "content": "Clothing",
    "amount": 1,
    "type": "box",
    "dimensions": {"length": 33, "width": 26, "height": 10},
    "weight": 0.5,
    "insurance": 0,
    "declaredValue": 0,
}

# Origin warehouse location (Aguascalientes, Mexico)
_ORIGIN_COUNTRY = "MX"
_ORIGIN_POSTAL_CODE = "20000"


def _is_configured() -> bool:
    settings = get_settings()
    return bool(settings.envia_api_key and not settings.envia_api_key.startswith("..."))


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {get_settings().envia_api_key}"}


async def get_shipping_rates(origin_zip: str, destination_zip: str) -> Decimal:
    """Return the lowest available shipping rate via envia.com.

    Uses the standard Vantier package dimensions (33×26×10 cm, 0.5 kg).
    Falls back to $9.99 stub rate when envia credentials are not configured.

    Args:
        origin_zip: Origin postal code (defaults to Aguascalientes warehouse).
        destination_zip: Customer destination postal code.

    Returns:
        Lowest available rate in USD as Decimal.

    Raises:
        AppException: If rate lookup fails with a configured key.
    """
    if not _is_configured():
        logger.info("STUB: Shipping rate %s -> %s = $9.99", origin_zip, destination_zip)
        return Decimal("9.99")

    settings = get_settings()
    payload = {
        "origin": {
            "country": _ORIGIN_COUNTRY,
            "postalCode": origin_zip,
        },
        "destination": {
            "country": "US",
            "postalCode": destination_zip,
        },
        "packages": [_PACKAGE],
        "shipment": {"carrier": "", "type": 1},
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.post(
                f"{settings.envia_base_url}/ship/rate/",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("envia.com rate API error %s: %s", exc.response.status_code, exc.response.text)
            raise AppException(f"Shipping rate lookup failed ({exc.response.status_code})", status_code=502) from exc
        except httpx.RequestError as exc:
            logger.error("envia.com network error: %s", exc)
            raise AppException("Shipping provider unreachable", status_code=502) from exc

    data = resp.json()
    rates = data.get("data", [])
    if not rates:
        logger.warning("envia.com returned no rates for %s -> %s", origin_zip, destination_zip)
        return Decimal("9.99")

    # Pick the cheapest option; prices returned by envia.com are in the carrier's currency.
    # For international (MX → US) carriers (FedEx/DHL), rates are quoted in USD.
    cheapest = min(rates, key=lambda r: float(r.get("totalPrice", 0)))
    price = Decimal(str(cheapest.get("totalPrice", "9.99")))
    logger.info("envia.com cheapest rate: %s %s via %s", price, cheapest.get("currency"), cheapest.get("carrier"))
    return price


async def create_shipment(order_id: str, address_data: dict) -> tuple[str, str]:
    """Generate a shipping label via envia.com.

    Args:
        order_id: Internal order UUID (used as reference in the shipment).
        address_data: JSONB shipping address dict with keys:
            full_name, line1, city, state, zip, country.

    Returns:
        Tuple of (tracking_number, label_url).

    Raises:
        AppException: If label generation fails.
    """
    if not _is_configured():
        logger.info("STUB: Creating shipment for order %s", order_id)
        return ("MOCK_TRK_" + order_id[:8], "https://envia.mock/label/" + order_id)

    settings = get_settings()
    payload = {
        "origin": {
            "name": "Vantier",
            "company": "Vantier",
            "email": settings.resend_support_email,
            "phone": "4491000000",
            "street": "Calle Principal 123",
            "number": "123",
            "district": "Centro",
            "city": "Aguascalientes",
            "state": "AGS",
            "country": _ORIGIN_COUNTRY,
            "postalCode": _ORIGIN_POSTAL_CODE,
            "reference": f"Order {order_id}",
        },
        "destination": {
            "name": address_data.get("full_name", ""),
            "street": address_data.get("line1", ""),
            "number": "",
            "district": address_data.get("city", ""),
            "city": address_data.get("city", ""),
            "state": address_data.get("state", ""),
            "country": address_data.get("country", "US"),
            "postalCode": address_data.get("zip", ""),
            "phone": "0000000000",
            "email": "",
        },
        "packages": [_PACKAGE],
        "shipment": {"carrier": "fedex", "type": 1},
        "settings": {"printFormat": "PDF", "printSize": "LETTER"},
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                f"{settings.envia_base_url}/ship/generate/",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("envia.com label API error %s: %s", exc.response.status_code, exc.response.text)
            raise AppException(f"Label generation failed ({exc.response.status_code})", status_code=502) from exc
        except httpx.RequestError as exc:
            logger.error("envia.com network error: %s", exc)
            raise AppException("Shipping provider unreachable", status_code=502) from exc

    data = resp.json()
    shipment = data.get("data", [{}])
    if isinstance(shipment, list):
        shipment = shipment[0] if shipment else {}

    tracking_number: str = shipment.get("trackingNumber") or shipment.get("tracking_number") or f"ENVIA_{order_id[:8]}"
    label_url: str = shipment.get("label") or shipment.get("label_url") or ""

    logger.info("envia.com label created: tracking=%s for order %s", tracking_number, order_id)
    return tracking_number, label_url
