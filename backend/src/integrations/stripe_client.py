"""Stripe integration — real Checkout Session creation and webhook verification."""

from __future__ import annotations

import logging

import stripe

from src.core.config import get_settings
from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


def _get_stripe() -> None:
    """Configure the Stripe SDK with the secret key from settings."""
    settings = get_settings()
    if not settings.stripe_secret_key or settings.stripe_secret_key.startswith("sk_test_..."):
        raise AppException("Stripe secret key not configured", status_code=503)
    stripe.api_key = settings.stripe_secret_key


async def create_checkout_session(
    order_id: str,
    items: list[dict],
    customer_email: str | None = None,
) -> tuple[str, str]:
    """Create a Stripe Checkout Session.

    Args:
        order_id: Internal order UUID (stored in session metadata).
        items: List of Stripe-formatted line items (price_data + quantity).
        customer_email: Pre-fills the email field on the Stripe Checkout page.

    Returns:
        Tuple of (checkout_url, session_id).
        checkout_url — the hosted Stripe Checkout URL to redirect the customer to.
        session_id   — Stripe's ``cs_...`` identifier; stored on the order for
                       webhook matching.

    Raises:
        AppException: If Stripe credentials are missing or the API call fails.
    """
    _get_stripe()
    settings = get_settings()

    kwargs: dict = {
        "payment_method_types": ["card"],
        "line_items": items,
        "mode": "payment",
        "success_url": f"{settings.frontend_url}/checkout/success?order={order_id}",
        "cancel_url": f"{settings.frontend_url}/checkout/cancel",
        "metadata": {"order_id": order_id},
    }
    if customer_email:
        kwargs["customer_email"] = customer_email

    try:
        session = await stripe.checkout.Session.create_async(**kwargs)
    except stripe.StripeError as exc:
        logger.error("Stripe API error creating session for order %s: %s", order_id, exc)
        raise AppException(f"Payment provider error: {exc.user_message}", status_code=502) from exc

    if not session.url:
        raise AppException("Stripe returned no checkout URL", status_code=502)

    logger.info("Stripe Checkout Session created: %s for order %s", session.id, order_id)
    return session.url, session.id


def verify_webhook_signature(payload: bytes, sig_header: str) -> bool:
    """Verify Stripe webhook signature using the configured webhook secret.

    Args:
        payload: Raw request body bytes (must NOT be decoded).
        sig_header: Value of the ``stripe-signature`` header.

    Returns:
        True if the signature is valid.

    Raises:
        AppException: If webhook secret is missing or signature is invalid.
    """
    settings = get_settings()
    if not settings.stripe_webhook_secret or settings.stripe_webhook_secret.startswith("whsec_..."):
        raise AppException("Stripe webhook secret not configured", status_code=503)

    try:
        stripe.WebhookSignature.verify_header(
            payload,
            sig_header,
            settings.stripe_webhook_secret,
            tolerance=300,
        )
        return True
    except stripe.SignatureVerificationError as exc:
        logger.warning("Stripe webhook signature verification failed: %s", exc)
        return False
