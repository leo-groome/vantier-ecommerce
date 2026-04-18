"""Resend transactional email client for Vantier."""

from __future__ import annotations

import logging

import httpx

from src.core.config import get_settings

logger = logging.getLogger(__name__)

_RESEND_BASE = "https://api.resend.com"

# ── Shared HTML layout ─────────────────────────────────────────────────────────

def _html(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#f5f4f0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f4f0;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #e0ddd7;max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="background:#0f0f0f;padding:28px 40px;text-align:center;">
              <span style="font-size:22px;font-weight:700;letter-spacing:4px;color:#f5f4f0;text-transform:uppercase;">VANTIER</span>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px;">
              {body}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f5f4f0;border-top:1px solid #e0ddd7;padding:24px 40px;text-align:center;">
              <p style="margin:0 0 6px;font-size:11px;color:#888;letter-spacing:1px;text-transform:uppercase;">Vantier Luxury LA</p>
              <p style="margin:0;font-size:11px;color:#aaa;">You received this email because you placed an order at vantierluxuryla.com</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _order_items_html(items: list[dict]) -> str:
    rows = ""
    for item in items:
        rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #f0ede8;font-size:14px;color:#333;">
            {item.get('qty', 1)}x &nbsp;{item.get('name', 'Item')}
          </td>
          <td style="padding:10px 0;border-bottom:1px solid #f0ede8;font-size:14px;color:#333;text-align:right;">
            ${item.get('price', '0.00')}
          </td>
        </tr>"""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
      {rows}
    </table>"""


# ── Internal POST ──────────────────────────────────────────────────────────────

async def _post(payload: dict) -> None:
    """Fire-and-forget POST to Resend /emails endpoint."""
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
            logger.info("Email sent: subject=%s to=%s", payload.get("subject"), payload.get("to"))
    except httpx.HTTPStatusError as exc:
        logger.error("Resend API error %s: %s", exc.response.status_code, exc.response.text)
    except Exception as exc:  # noqa: BLE001
        logger.error("Resend email failed: %s", exc)


# ── Transactional emails ───────────────────────────────────────────────────────

async def send_order_confirmed(
    order_id: str, customer_email: str, items: list[dict], total_usd: str, estimated_shipping: str
) -> None:
    settings = get_settings()
    short_id = order_id[:8].upper()
    items_html = _order_items_html(items)

    body = f"""
      <p style="margin:0 0 4px;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#999;">Order Confirmed</p>
      <h1 style="margin:0 0 24px;font-size:26px;font-weight:700;color:#0f0f0f;letter-spacing:1px;">Thank you for your order</h1>

      <p style="margin:0 0 20px;font-size:14px;color:#555;line-height:1.6;">
        We've received your order and it's being prepared. You'll receive a shipping notification once it's on its way.
      </p>

      <div style="background:#f5f4f0;border:1px solid #e0ddd7;padding:16px 20px;margin:0 0 24px;">
        <p style="margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#999;">Order Reference</p>
        <p style="margin:4px 0 0;font-size:16px;font-weight:600;color:#0f0f0f;font-family:monospace;">#{short_id}</p>
      </div>

      {items_html}

      <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px;">
        <tr>
          <td style="padding:8px 0;font-size:13px;color:#777;">Shipping</td>
          <td style="padding:8px 0;font-size:13px;color:#777;text-align:right;">
            {"Free" if estimated_shipping == "0.00" or estimated_shipping == "0" else f"${estimated_shipping}"}
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;font-size:15px;font-weight:700;color:#0f0f0f;border-top:2px solid #0f0f0f;">Total</td>
          <td style="padding:8px 0;font-size:15px;font-weight:700;color:#0f0f0f;text-align:right;border-top:2px solid #0f0f0f;">${total_usd}</td>
        </tr>
      </table>

      <p style="margin:28px 0 0;font-size:13px;color:#777;line-height:1.6;">
        Estimated delivery: <strong>5–7 business days</strong><br/>
        Questions? Reply to this email or visit <a href="https://vantierluxuryla.com" style="color:#0f0f0f;">vantierluxuryla.com</a>
      </p>
    """

    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email],
        "reply_to": settings.resend_support_email,
        "subject": f"Your Vantier order is confirmed — #{short_id}",
        "html": _html("Order Confirmed — Vantier", body),
        "text": f"Order confirmed #{short_id}\n\nTotal: ${total_usd}\nEst. delivery: 5–7 business days\n\nThank you for shopping with Vantier.",
    })


async def send_order_shipped(customer_email: str, tracking_number: str, carrier: str) -> None:
    settings = get_settings()
    body = f"""
      <p style="margin:0 0 4px;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#999;">Shipped</p>
      <h1 style="margin:0 0 24px;font-size:26px;font-weight:700;color:#0f0f0f;">Your order is on its way</h1>
      <p style="margin:0 0 20px;font-size:14px;color:#555;line-height:1.6;">Good news — your Vantier order has been shipped.</p>
      <div style="background:#f5f4f0;border:1px solid #e0ddd7;padding:16px 20px;margin:0 0 24px;">
        <p style="margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#999;">Carrier</p>
        <p style="margin:4px 0 12px;font-size:14px;font-weight:600;color:#0f0f0f;">{carrier}</p>
        <p style="margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#999;">Tracking Number</p>
        <p style="margin:4px 0 0;font-size:14px;font-weight:600;color:#0f0f0f;font-family:monospace;">{tracking_number}</p>
      </div>
      <p style="margin:0;font-size:13px;color:#777;">Allow 24–48 hours for tracking to activate.</p>
    """
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email],
        "reply_to": settings.resend_support_email,
        "subject": "Your Vantier order has shipped",
        "html": _html("Your Order Has Shipped — Vantier", body),
        "text": f"Your order has shipped.\n\nCarrier: {carrier}\nTracking: {tracking_number}",
    })


async def send_low_stock_alert(variants: list[dict]) -> None:
    if not variants:
        return
    settings = get_settings()
    rows = "\n".join(
        f"  • {v['sku']} ({v['style']} / {v['size']} / {v['color']}) — {v['stock_qty']} units left"
        for v in variants
    )
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [settings.resend_support_email],
        "subject": f"Low Stock Alert — {len(variants)} variant(s) need attention",
        "text": f"Low Stock Alert\n\n{rows}\n\nReview inventory and issue a purchase order if needed.",
    })


async def send_exchange_notification(
    order_id: str, customer_email: str, admin_email: str, exchange_details: str
) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [customer_email, admin_email],
        "subject": f"Exchange Request — Order #{order_id[:8].upper()}",
        "text": f"Exchange requested for Order #{order_id}.\n\n{exchange_details}",
    })


async def send_new_order_alert(order_id: str, summary: str) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [settings.resend_support_email],
        "subject": f"New Order — #{order_id[:8].upper()}",
        "text": f"New order placed.\n\n{summary}",
    })


async def send_contact_form(sender_name: str, sender_email: str, message: str) -> None:
    settings = get_settings()
    await _post({
        "from": f"Vantier <{settings.resend_from_email}>",
        "to": [settings.resend_support_email],
        "reply_to": sender_email,
        "subject": f"Contact: {sender_name}",
        "text": f"Name: {sender_name}\nEmail: {sender_email}\n\n{message}",
    })
