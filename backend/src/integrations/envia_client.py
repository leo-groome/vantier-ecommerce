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


def _stub_rates() -> list[dict]:
    """Return mock shipping options when envia credentials are not configured."""
    return [
        {
            "carrier_id": "fedex-economy",
            "carrier_name": "FedEx",
            "service": "Economy",
            "price_usd": 9.99,
            "estimated_days": 5,
        },
        {
            "carrier_id": "fedex-express",
            "carrier_name": "FedEx",
            "service": "Express",
            "price_usd": 19.99,
            "estimated_days": 2,
        },
    ]


async def get_shipping_rates(origin_zip: str, destination_zip: str) -> list[dict]:
    """Return all available shipping options via envia.com.

    Each option includes carrier, service, price in USD and estimated delivery days.
    Uses the standard Vantier package dimensions (33×26×10 cm, 0.5 kg).
    Falls back to mock options when envia credentials are not configured.

    Args:
        origin_zip: Origin postal code (Aguascalientes warehouse).
        destination_zip: Customer destination postal code.

    Returns:
        List of rate dicts with keys: carrier_id, carrier_name, service,
        price_usd (float), estimated_days (int).

    Raises:
        AppException: If rate lookup fails with a configured key.
    """
    if not _is_configured():
        logger.info("STUB: Shipping rates %s -> %s (mock)", origin_zip, destination_zip)
        return _stub_rates()

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

    raw_rates: list[dict] = resp.json().get("data", [])
    if not raw_rates:
        logger.warning("envia.com returned no rates for %s -> %s", origin_zip, destination_zip)
        return _stub_rates()

    # Normalize envia response to internal format. International (MX→US) rates
    # from FedEx/DHL are quoted in USD.
    result: list[dict] = []
    for r in raw_rates:
        carrier = str(r.get("carrier", "")).lower()
        service = str(r.get("service", r.get("serviceName", "Standard")))
        carrier_id = f"{carrier}-{service.lower().replace(' ', '-')}"
        result.append({
            "carrier_id": carrier_id,
            "carrier_name": str(r.get("carrier", carrier)).upper(),
            "service": service,
            "price_usd": float(r.get("totalPrice", 9.99)),
            "estimated_days": int(r.get("days", r.get("deliveryDays", 5))),
        })

    result.sort(key=lambda x: x["price_usd"])
    logger.info("envia.com returned %d rates for %s -> %s", len(result), origin_zip, destination_zip)
    return result


async def get_cheapest_rate(origin_zip: str, destination_zip: str) -> Decimal:
    """Return only the cheapest rate as a Decimal (used internally by order service).

    Args:
        origin_zip: Origin postal code.
        destination_zip: Customer destination postal code.

    Returns:
        Cheapest rate in USD as Decimal.
    """
    rates = await get_shipping_rates(origin_zip, destination_zip)
    return Decimal(str(rates[0]["price_usd"])) if rates else Decimal("9.99")


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
