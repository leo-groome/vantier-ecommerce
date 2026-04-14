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
