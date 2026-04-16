"""Business logic for the orders feature slice."""

from __future__ import annotations

import logging
import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.exceptions import ConflictException, NotFoundException, StockInsufficientException
from src.features.orders.models import Order, OrderItem
from src.features.orders.schemas import OrderCreate
from src.features.products.models import ProductVariant
from src.integrations import envia_client, resend_client, stripe_client

logger = logging.getLogger(__name__)

# Valid state transitions: current_status → allowed next statuses
_VALID_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"processing", "cancelled"},
    "processing": {"shipped", "cancelled"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
}


# ── Checkout ───────────────────────────────────────────────────────────────────

async def create_order(
    db: AsyncSession,
    user_id: str | None,
    data: OrderCreate,
) -> tuple[Order, str]:
    """Create a new order and return (order, stripe_checkout_url).

    Validates stock (read-only). Stock is NOT decremented here — that happens
    in confirm_payment() when Stripe confirms the payment via webhook.

    Args:
        db: Async database session.
        user_id: Neon Auth user ID; None for guest checkout.
        data: Validated order creation data.

    Returns:
        Tuple of (created Order ORM instance, Stripe checkout URL string).

    Raises:
        NotFoundException: If any variant does not exist or is inactive.
        StockInsufficientException: If any item qty exceeds available stock.
        ConflictException: If discount code is invalid, expired, or limit reached.
    """
    # ── 1. Load and validate variants ─────────────────────────────────────────
    variant_ids = [item.variant_id for item in data.items]
    result = await db.execute(
        select(ProductVariant).where(
            ProductVariant.id.in_(variant_ids),
            ProductVariant.is_active.is_(True),
        )
    )
    variants: dict[uuid.UUID, ProductVariant] = {v.id: v for v in result.scalars().all()}

    for item in data.items:
        if item.variant_id not in variants:
            raise NotFoundException(f"Variant {item.variant_id} not found or inactive")

    # ── 2. Validate stock (read-only — no decrement yet) ──────────────────────
    for item in data.items:
        variant = variants[item.variant_id]
        if int(variant.stock_qty) < item.qty:
            raise StockInsufficientException(
                f"Insufficient stock for variant {item.variant_id}: "
                f"requested {item.qty}, available {int(variant.stock_qty)}"
            )

    # ── 3. Compute subtotal ───────────────────────────────────────────────────
    subtotal_usd: Decimal = sum(
        variants[item.variant_id].price_usd * item.qty for item in data.items
    )
    total_qty = sum(item.qty for item in data.items)

    # ── 4. Shipping ───────────────────────────────────────────────────────────
    if total_qty >= 5:
        is_free_shipping = True
        shipping_usd = Decimal("0.00")
    else:
        is_free_shipping = False
        shipping_usd = await envia_client.get_shipping_rates(
            origin_zip="20000",
            destination_zip=data.shipping_address.zip,
        )

    # ── 5. Discount ───────────────────────────────────────────────────────────
    discount_usd = Decimal("0.00")
    discount_code_id: uuid.UUID | None = None

    if data.discount_code:
        from src.features.discounts import service as discounts_service
        from src.features.discounts.models import DiscountCode
        from src.features.discounts.schemas import DiscountValidateRequest

        # Resolve code ID first (simple lookup — validation below does FOR UPDATE)
        code_result = await db.execute(
            select(DiscountCode).where(
                func.upper(DiscountCode.code) == data.discount_code.upper(),
                DiscountCode.is_active.is_(True),
            )
        )
        code_obj = code_result.scalar_one_or_none()
        if code_obj is None:
            raise NotFoundException(f"Discount code '{data.discount_code}' not found or inactive")
        discount_code_id = code_obj.id

        # Full validation (expiry + usage limit, using FOR UPDATE)
        validate_resp = await discounts_service.validate_discount_code(
            db,
            DiscountValidateRequest(
                code=data.discount_code,
                order_subtotal_usd=subtotal_usd,
            ),
        )
        discount_usd = validate_resp.discount_amount_usd

    # ── 6. Total ──────────────────────────────────────────────────────────────
    total_usd = max(subtotal_usd + shipping_usd - discount_usd, Decimal("0.00"))

    # ── 7. Create Order record ────────────────────────────────────────────────
    order = Order(
        neon_auth_user_id=user_id,
        customer_email=str(data.customer_email),
        customer_name=data.customer_name,
        status="pending",
        payment_status="pending",
        subtotal_usd=subtotal_usd,
        shipping_usd=shipping_usd,
        discount_usd=discount_usd,
        total_usd=total_usd,
        is_free_shipping=is_free_shipping,
        shipping_address=data.shipping_address.model_dump(),
        discount_code_id=discount_code_id,
    )
    db.add(order)
    await db.flush()  # Materialize UUID before creating items

    # ── 8. Create OrderItems (price frozen at order time) ─────────────────────
    for item in data.items:
        variant = variants[item.variant_id]
        db.add(OrderItem(
            order_id=order.id,
            variant_id=item.variant_id,
            qty=item.qty,
            unit_price_usd=variant.price_usd,
        ))

    # ── 9. Create Stripe Checkout Session ─────────────────────────────────────
    stripe_items = [
        {
            "price_data": {
                "currency": "usd",
                "unit_amount": int(variants[item.variant_id].price_usd * 100),
                "product_data": {"name": variants[item.variant_id].sku},
            },
            "quantity": item.qty,
        }
        for item in data.items
    ]
    checkout_url = await stripe_client.create_checkout_session(
        str(order.id), stripe_items, str(data.customer_email)
    )
    # Store session ID extracted from the URL (stub: last path segment = order UUID).
    # Production: Stripe SDK returns Session.id directly (cs_xxx).
    order.stripe_checkout_session_id = checkout_url.rstrip("/").split("/")[-1]

    await db.flush()
    return order, checkout_url


# ── Webhook ────────────────────────────────────────────────────────────────────

async def confirm_payment(db: AsyncSession, checkout_session_id: str) -> Order | None:
    """Process a confirmed Stripe payment: decrement stock and mark order paid.

    Called by the Stripe webhook when checkout.session.completed fires.
    Idempotent: if the order is already paid, returns it unchanged.

    Args:
        db: Async database session.
        checkout_session_id: Stripe Checkout Session ID from the webhook event.

    Returns:
        Updated Order, or None if the session_id is unknown (unrelated event).
    """
    result = await db.execute(
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.stripe_checkout_session_id == checkout_session_id)
    )
    order = result.unique().scalar_one_or_none()
    if order is None:
        return None

    # Idempotency: already processed
    if order.payment_status == "paid":
        return order

    # ── Decrement stock atomically (FOR UPDATE) ───────────────────────────────
    variant_ids = [item.variant_id for item in order.items]
    variants_result = await db.execute(
        select(ProductVariant)
        .where(ProductVariant.id.in_(variant_ids))
        .with_for_update()
    )
    variants: dict[uuid.UUID, ProductVariant] = {
        v.id: v for v in variants_result.scalars().all()
    }

    for item in order.items:
        variant = variants.get(item.variant_id)
        if variant is None:
            logger.error(
                "Variant %s missing during stock decrement for order %s — skipping",
                item.variant_id, order.id,
            )
            continue
        new_stock = int(variant.stock_qty) - int(item.qty)
        if new_stock < 0:
            # Payment is already confirmed — cannot fail here; flag for manual review
            logger.error(
                "Stock underflow for variant %s (order %s): current=%s, requested=%s. "
                "Clamping to 0 — manual review required.",
                item.variant_id, order.id, variant.stock_qty, item.qty,
            )
            new_stock = 0
        variant.stock_qty = new_stock

    # ── Increment discount usage count ───────────────────────────────────────
    if order.discount_code_id is not None:
        from src.features.discounts import service as discounts_service

        try:
            await discounts_service.increment_usage_count(db, order.discount_code_id)
        except ConflictException:
            # Usage limit race: another order beat us. Payment is confirmed regardless.
            logger.warning(
                "Discount code usage limit already reached for order %s — skipping increment",
                order.id,
            )

    # ── Update order state ────────────────────────────────────────────────────
    order.payment_status = "paid"
    order.status = "processing"
    await db.flush()

    # ── Transactional emails (fire-and-forget; never raise) ───────────────────
    items_summary = [
        {
            "qty": int(item.qty),
            "name": str(item.variant_id),
            "price": str(item.unit_price_usd),
        }
        for item in order.items
    ]
    await resend_client.send_order_confirmed(
        str(order.id),
        order.customer_email,
        items_summary,
        str(order.total_usd),
        str(order.shipping_usd),
    )
    await resend_client.send_new_order_alert(
        str(order.id),
        f"Customer: {order.customer_email}\nTotal: ${order.total_usd}\nItems: {len(order.items)}",
    )

    return order


# ── Read ───────────────────────────────────────────────────────────────────────

async def get_order(db: AsyncSession, order_id: uuid.UUID) -> Order:
    """Fetch a single order with items eagerly loaded.

    Args:
        db: Async database session.
        order_id: Order UUID.

    Returns:
        Order ORM instance with items populated.

    Raises:
        NotFoundException: If order not found.
    """
    result = await db.execute(
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.id == order_id)
    )
    order = result.unique().scalar_one_or_none()
    if order is None:
        raise NotFoundException(f"Order {order_id} not found")
    return order


async def get_order_for_user(
    db: AsyncSession, order_id: uuid.UUID, user_id: str
) -> Order:
    """Fetch an order, verifying it belongs to the authenticated user.

    Args:
        db: Async database session.
        order_id: Order UUID.
        user_id: Neon Auth user ID to verify ownership.

    Returns:
        Order ORM instance with items populated.

    Raises:
        NotFoundException: If order not found or belongs to a different user.
    """
    result = await db.execute(
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.id == order_id, Order.neon_auth_user_id == user_id)
    )
    order = result.unique().scalar_one_or_none()
    if order is None:
        raise NotFoundException(f"Order {order_id} not found")
    return order


async def list_orders(
    db: AsyncSession,
    status: str | None = None,
    customer_email: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> list[Order]:
    """List all orders for admin with optional filters.

    Args:
        db: Async database session.
        status: Filter by order status (exact match).
        customer_email: Filter by customer email (case-insensitive partial match).
        page: 1-based page number.
        page_size: Results per page.

    Returns:
        List of Orders ordered by creation date descending, with items loaded.
    """
    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
    )
    if status:
        stmt = stmt.where(Order.status == status)
    if customer_email:
        stmt = stmt.where(Order.customer_email.ilike(f"%{customer_email}%"))

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    return list(result.unique().scalars().all())


async def list_user_orders(db: AsyncSession, user_id: str) -> list[Order]:
    """List all orders for an authenticated storefront customer.

    Args:
        db: Async database session.
        user_id: Neon Auth user ID.

    Returns:
        List of Orders ordered by creation date descending, with items loaded.
    """
    result = await db.execute(
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.neon_auth_user_id == user_id)
        .order_by(Order.created_at.desc())
    )
    return list(result.unique().scalars().all())


# ── Admin mutations ────────────────────────────────────────────────────────────

async def update_order_status(
    db: AsyncSession, order_id: uuid.UUID, new_status: str
) -> Order:
    """Transition order status following the valid state machine.

    Valid transitions:
    - pending → processing | cancelled
    - processing → shipped | cancelled
    - shipped → delivered

    Fires send_order_shipped email when transitioning to 'shipped' (if tracking exists).

    Args:
        db: Async database session.
        order_id: Order UUID.
        new_status: Target status string.

    Returns:
        Updated Order.

    Raises:
        NotFoundException: If order not found.
        ConflictException: If the transition is not permitted.
    """
    order = await get_order(db, order_id)

    allowed = _VALID_TRANSITIONS.get(order.status, set())
    if new_status not in allowed:
        raise ConflictException(
            f"Cannot transition order from '{order.status}' to '{new_status}'"
        )

    order.status = new_status
    await db.flush()

    if new_status == "shipped" and order.carrier_tracking_number:
        await resend_client.send_order_shipped(
            order.customer_email,
            order.carrier_tracking_number,
            carrier="envia.com",
        )

    return order


async def generate_shipping_label(db: AsyncSession, order_id: uuid.UUID) -> Order:
    """Generate a shipping label via envia.com and store tracking info on the order.

    Args:
        db: Async database session.
        order_id: Order UUID.

    Returns:
        Updated Order with carrier_tracking_number, envia_shipment_id, and envia_label_url set.

    Raises:
        NotFoundException: If order not found.
    """
    order = await get_order(db, order_id)

    tracking_number, label_url = await envia_client.create_shipment(
        str(order.id), order.shipping_address
    )

    order.carrier_tracking_number = tracking_number
    order.envia_shipment_id = tracking_number  # stub returns same value; prod would be distinct
    order.envia_label_url = label_url

    await db.flush()
    return order
