"""Resend transactional email client for Vantier."""

from __future__ import annotations

import logging

import httpx

from src.core.config import get_settings

logger = logging.getLogger(__name__)

_RESEND_BASE = "https://api.resend.com"


async def _post(payload: dict) -> None:
    """Fire-and-forget POST to Resend /emails endpoint.

    Logs errors but does NOT raise, so email failures never break the main flow.
    """
    try:
        settings = get_settings()
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{_RESEND_BASE}/emails",
                headers={
                    "Authorization": f"Bearer {settings.resend_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        logger.error("Resend email failed: %s", exc)


async def send_low_stock_alert(variants: list[dict]) -> None:
    """Notify the owner that one or more variants have hit the low-stock threshold.

    Args:
        variants: List of dicts with keys: sku, size, color, style, stock_qty.
    """
    if not variants:
        return

    settings = get_settings()
    rows = "\n".join(
        f"  • {v['sku']} ({v['style']} / {v['size']} / {v['color']}) — {v['stock_qty']} units left"
        for v in variants
    )
    body = (
        "⚠️ Low Stock Alert — Vantier\n\n"
        "The following variants have reached or dropped below 50 units:\n\n"
        f"{rows}\n\n"
        "Please review your inventory and issue a purchase order if needed."
    )

    await _post(
        {
            "from": f"Vantier <{settings.resend_from_email}>",
            "to": [settings.resend_support_email],
            "subject": f"⚠️ Low Stock Alert — {len(variants)} variant(s) need attention",
            "text": body,
        }
    )


async def send_order_confirmed(
    order_id: str, customer_email: str, items: list[dict], total_usd: str, estimated_shipping: str
) -> None:
    settings = get_settings()
    item_rows = "\n".join(f" - {i['qty']}x {i['name']} (${i['price']})" for i in items)
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email],
        "subject": f"Order Confirmed - #{order_id}",
        "text": f"Thank you for your order!\n\nOrder #{order_id}\nTotal: ${total_usd}\nEst. Shipping: {estimated_shipping}\n\nItems:\n{item_rows}"
    })


async def send_order_shipped(
    customer_email: str, tracking_number: str, carrier: str
) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email],
        "subject": "Your Vantier Order Has Shipped",
        "text": f"Your order is on the way!\n\nCarrier: {carrier}\nTracking Number: {tracking_number}"
    })


async def send_exchange_notification(
    order_id: str, customer_email: str, admin_email: str, exchange_details: str
) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email, admin_email],
        "subject": f"Exchange Requested - Order #{order_id}",
        "text": f"An exchange has been requested for Order #{order_id}.\n\nDetails:\n{exchange_details}"
    })


async def send_new_order_alert(order_id: str, summary: str) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [settings.resend_support_email],
        "subject": f"New Order Received - #{order_id}",
        "text": f"A new order has been placed.\n\n{summary}"
    })


async def send_contact_form(
    sender_name: str, sender_email: str, message: str
) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [settings.resend_support_email],
        "reply_to": sender_email,
        "subject": f"New Contact Request from {sender_name}",
        "text": f"You have received a new contact form submission.\n\nName: {sender_name}\nEmail: {sender_email}\nMessage:\n{message}"
    })
