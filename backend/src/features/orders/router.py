"""FastAPI router for the orders feature slice."""

from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Query, Request

from src.core.dependencies import AdminUserDep, CurrentUser, DBSession
from src.core.exceptions import AppException
from src.features.orders import service
from src.features.orders.schemas import (
    CheckoutResponse,
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    PaymentIntentResponse,
)
from src.integrations import stripe_client

router = APIRouter()


# ── Public endpoints ───────────────────────────────────────────────────────────

@router.post("/checkout", response_model=CheckoutResponse, status_code=201)
async def checkout(
    data: OrderCreate,
    db: DBSession,
) -> CheckoutResponse:
    """Create an order and return a Stripe Checkout Session URL.

    Public endpoint — no authentication required (supports guest checkout).
    Stock is validated but NOT decremented here; that happens on payment confirmation.
    """
    # Resolve optional user identity from request if auth header present (best-effort)
    order, checkout_url = await service.create_order(db, user_id=None, data=data)
    return CheckoutResponse(order_id=order.id, checkout_url=checkout_url)


@router.get("/confirmation/{order_id}", response_model=OrderResponse)
async def get_order_confirmation(
    order_id: uuid.UUID,
    db: DBSession,
) -> OrderResponse:
    """Fetch a confirmed (paid) order for the post-payment success screen.

    Public endpoint — secured by UUID opacity. Only returns paid orders.
    """
    order = await service.get_order_confirmation(db, order_id)
    if order is None:
        raise AppException("Order not found or payment not confirmed yet", status_code=404, error_code="NOT_FOUND")
    return OrderResponse.model_validate(order)


@router.post("/create-payment-intent", response_model=PaymentIntentResponse, status_code=201)
async def create_payment_intent(
    data: OrderCreate,
    db: DBSession,
) -> PaymentIntentResponse:
    """Create an order and return a Stripe PaymentIntent client_secret for embedded checkout.

    Public endpoint — no authentication required (supports guest checkout).
    Stock is validated but NOT decremented here; that happens on payment confirmation.
    """
    order, client_secret, amount_cents = await service.create_order_with_payment_intent(
        db, user_id=None, data=data
    )
    return PaymentIntentResponse(
        order_id=order.id,
        client_secret=client_secret,
        amount_cents=amount_cents,
    )


@router.post("/webhook/stripe", status_code=200)
async def stripe_webhook(request: Request, db: DBSession) -> dict:
    """Stripe webhook receiver for payment confirmation events.

    Public endpoint — secured via Stripe signature verification.
    On checkout.session.completed: decrements stock, marks order paid,
    sends confirmation emails.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not stripe_client.verify_webhook_signature(payload, sig_header):
        raise AppException("Invalid Stripe webhook signature", status_code=400, error_code="INVALID_SIGNATURE")

    try:
        event = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise AppException("Invalid webhook payload", status_code=400, error_code="BAD_REQUEST") from exc

    event_type = event.get("type", "")
    obj = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        session_id = obj.get("id", "")
        if session_id:
            await service.confirm_payment(db, session_id)

    elif event_type == "payment_intent.succeeded":
        payment_intent_id = obj.get("id", "")
        if payment_intent_id:
            await service.confirm_payment_by_intent(db, payment_intent_id)

    return {"ok": True}


# ── Customer endpoints (requires Neon Auth JWT) ────────────────────────────────

@router.get("/my", response_model=list[OrderResponse])
async def list_my_orders(
    db: DBSession,
    current_user: CurrentUser,
) -> list[OrderResponse]:
    """List all orders for the authenticated storefront customer."""
    orders = await service.list_user_orders(db, current_user["sub"])
    return [OrderResponse.model_validate(o) for o in orders]


@router.get("/my/{order_id}", response_model=OrderResponse)
async def get_my_order(
    order_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> OrderResponse:
    """Fetch a specific order for the authenticated customer (ownership enforced)."""
    order = await service.get_order_for_user(db, order_id, current_user["sub"])
    return OrderResponse.model_validate(order)


# ── Admin endpoints ────────────────────────────────────────────────────────────

@router.get("", response_model=list[OrderResponse])
async def list_orders(
    db: DBSession,
    _admin: AdminUserDep,
    status: str | None = Query(None, description="Filter by order status"),
    customer_email: str | None = Query(None, description="Filter by customer email (partial match)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> list[OrderResponse]:
    """List all orders with optional filters. Requires admin role."""
    orders = await service.list_orders(
        db,
        status=status,
        customer_email=customer_email,
        page=page,
        page_size=page_size,
    )
    return [OrderResponse.model_validate(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> OrderResponse:
    """Fetch any order by ID. Requires admin role."""
    order = await service.get_order(db, order_id)
    return OrderResponse.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: uuid.UUID,
    data: OrderStatusUpdate,
    db: DBSession,
    _admin: AdminUserDep,
) -> OrderResponse:
    """Transition an order's status. Requires admin role.

    Valid transitions: pending→processing, processing→shipped,
    processing→cancelled, shipped→delivered.
    """
    order = await service.update_order_status(db, order_id, data.status)
    return OrderResponse.model_validate(order)


@router.post("/{order_id}/shipping-label", response_model=OrderResponse)
async def generate_shipping_label(
    order_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> OrderResponse:
    """Generate a shipping label via envia.com and store tracking info. Requires admin role."""
    order = await service.generate_shipping_label(db, order_id)
    return OrderResponse.model_validate(order)
