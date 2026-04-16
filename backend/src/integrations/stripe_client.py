"""Stripe integration stubs."""

from __future__ import annotations

import logging

from src.core.config import get_settings
from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


async def create_checkout_session(
    order_id: str,
    items: list[dict],
    customer_email: str | None = None
) -> str:
    """Create a Stripe Checkout session.
    
    Returns the Checkout Session URL.
    """
    settings = get_settings()
    if settings.is_production:
        raise AppException("Stripe integration missing credentials", status_code=503)
        
    logger.info(f"STUB: Creating Stripe Checkout for order {order_id}")
    return f"https://checkout.stripe.mock/{order_id}"


def verify_webhook_signature(payload: bytes, sig_header: str) -> bool:
    """Verify Stripe webhook signature."""
    settings = get_settings()
    if settings.is_production:
        raise AppException("Stripe integration missing credentials", status_code=503)
        
    logger.info("STUB: Verifying Stripe Webhook Signature")
    return True
