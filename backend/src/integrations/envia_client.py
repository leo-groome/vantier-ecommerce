"""Envia.com integration — shipping rate lookup and label generation."""

from __future__ import annotations

import asyncio
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
_ORIGIN_CITY = "Aguascalientes"
_ORIGIN_STATE = "AGS"
_ORIGIN_DISTRICT = "Centro"  # Required by Paquetexpress

# Envia requires Mexico state abbreviations, not full names.
# Maps common spellings/full names → official Envia codes.
_MX_STATE_CODES: dict[str, str] = {
    "aguascalientes": "AGS",
    "baja california": "BC", "baja california norte": "BC",
    "baja california sur": "BCS",
    "campeche": "CAMP",
    "chiapas": "CHIS",
    "chihuahua": "CHIH",
    "ciudad de mexico": "DF", "cdmx": "DF", "df": "DF",
    "distrito federal": "DF",
    "coahuila": "COAH", "coahuila de zaragoza": "COAH",
    "colima": "COL",
    "durango": "DGO",
    "guanajuato": "GTO",
    "guerrero": "GRO",
    "hidalgo": "HGO",
    "jalisco": "JAL",
    "mexico": "MEX", "estado de mexico": "MEX", "edomex": "MEX",
    "michoacan": "MICH", "michoacán": "MICH", "michoacan de ocampo": "MICH",
    "morelos": "MOR",
    "nayarit": "NAY",
    "nuevo leon": "NL", "nuevo león": "NL",
    "oaxaca": "OAX",
    "puebla": "PUE",
    "queretaro": "QRO", "querétaro": "QRO",
    "quintana roo": "QROO",
    "san luis potosi": "SLP", "san luis potosí": "SLP",
    "sinaloa": "SIN",
    "sonora": "SON",
    "tabasco": "TAB",
    "tamaulipas": "TAMPS",
    "tlaxcala": "TLAX",
    "veracruz": "VER", "veracruz de ignacio de la llave": "VER",
    "yucatan": "YUC", "yucatán": "YUC",
    "zacatecas": "ZAC",
}


def _normalize_mx_state(state: str) -> str:
    """Convert a Mexico state name or code to the abbreviation Envia expects."""
    key = state.strip().lower()
    return _MX_STATE_CODES.get(key, state.upper())


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


async def get_shipping_rates(
    origin_zip: str,
    destination_zip: str,
    destination_country: str = "US",
    destination_city: str = "",
    destination_state: str = "",
    destination_district: str = "",
) -> list[dict]:
    """Return all available shipping options via envia.com.

    Each option includes carrier, service, price in USD and estimated delivery days.
    Uses the standard Vantier package dimensions (33×26×10 cm, 0.5 kg).
    Falls back to mock options when envia credentials are not configured.

    Args:
        origin_zip: Origin postal code (Aguascalientes warehouse).
        destination_zip: Customer destination postal code.
        destination_country: ISO2 country code for the destination.
        destination_city: Customer city (improves rate accuracy).
        destination_state: Customer state/province code (improves rate accuracy).

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
    destination: dict = {
        "country": destination_country,
        "postalCode": destination_zip,
        "city": destination_city or "N/A",
        "state": (
            _normalize_mx_state(destination_state)
            if destination_country == "MX"
            else destination_state
        ),
    }
    if destination_district:
        destination["district"] = destination_district

    # Envia requires one request per carrier. Query in parallel and merge results.
    # paquetexpress requires destination district (colonia); only include it when provided.
    _CARRIERS = ["fedex", "dhl", "ups"] + (["paquetexpress"] if destination_district else [])

    async def _fetch_carrier(client: httpx.AsyncClient, carrier: str) -> list[dict]:
        payload = {
            "origin": {
                "country": _ORIGIN_COUNTRY,
                "postalCode": origin_zip,
                "city": _ORIGIN_CITY,
                "state": _ORIGIN_STATE,
                "district": _ORIGIN_DISTRICT,
            },
            "destination": destination,
            "packages": [_PACKAGE],
            "shipment": {"carrier": carrier, "type": 1},
        }
        try:
            resp = await client.post(
                f"{settings.envia_base_url}/ship/rate/",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            body = resp.json()
            rates: list[dict] = body.get("data", [])
            if not isinstance(rates, list):
                return []
            return rates
        except Exception as exc:
            logger.debug("envia.com carrier=%s skipped: %s", carrier, exc)
            return []

    async with httpx.AsyncClient(timeout=15.0) as client:
        results = await asyncio.gather(*[_fetch_carrier(client, c) for c in _CARRIERS])

    raw_rates: list[dict] = [r for carrier_rates in results for r in carrier_rates]

    if not raw_rates:
        logger.warning("envia.com returned no rates for %s -> %s (carriers: %s)", origin_zip, destination_zip, _CARRIERS)
        return []

    # Normalize to internal format.
    result: list[dict] = []
    for r in raw_rates:
        carrier = str(r.get("carrier", "")).lower()
        service = str(r.get("service", r.get("serviceName", "Standard")))
        carrier_id = f"{carrier}-{service.lower().replace(' ', '-')}"
        result.append({
            "carrier_id": carrier_id,
            "carrier_name": str(r.get("carrier", carrier)).upper(),
            "service": service,
            "price_usd": float(r.get("totalPrice") or r.get("price") or 0.0),
            "estimated_days": int(r.get("days") or r.get("deliveryDays") or r.get("estimatedDays") or 7),
        })

    result.sort(key=lambda x: x["price_usd"])
    logger.info("envia.com returned %d rates for %s -> %s", len(result), origin_zip, destination_zip)
    return result


async def get_cheapest_rate(origin_zip: str, destination_zip: str, destination_country: str = "US") -> Decimal:
    """Return only the cheapest rate as a Decimal (used internally by order service).

    Args:
        origin_zip: Origin postal code.
        destination_zip: Customer destination postal code.
        destination_country: Customer destination country code.

    Returns:
        Cheapest rate in USD as Decimal.
    """
    rates = await get_shipping_rates(origin_zip, destination_zip, destination_country)
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
