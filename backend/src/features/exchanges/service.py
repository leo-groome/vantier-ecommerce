"""Business logic for the exchanges feature slice."""

from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import ConflictException, NotFoundException
from src.features.exchanges.models import Exchange
from src.features.exchanges.schemas import ExchangeAdminUpdate, ExchangeCreate
from src.features.orders.models import Order, OrderItem
from src.features.products.models import ProductVariant
from src.integrations import resend_client


async def list_exchanges(db: AsyncSession) -> list[Exchange]:
    """Return all exchanges ordered by creation date descending."""
    result = await db.execute(
        select(Exchange).order_by(Exchange.created_at.desc())
    )
    return list(result.scalars().all())


async def get_exchange(db: AsyncSession, exchange_id: uuid.UUID) -> Exchange:
    """Fetch a single exchange by UUID.

    Raises:
        NotFoundException: If not found.
    """
    result = await db.execute(
        select(Exchange).where(Exchange.id == exchange_id)
    )
    obj = result.scalar_one_or_none()
    if obj is None:
        raise NotFoundException(f"Exchange {exchange_id} not found")
    return obj


async def create_exchange(db: AsyncSession, data: ExchangeCreate) -> Exchange:
    """Create a new exchange request from a customer.

    Validates:
    - Order exists.
    - original_variant_id is in the order's items.
    - No pending/approved exchange already open for same order+variant.

    Fires Resend notification (fire-and-forget — never raises).

    Raises:
        NotFoundException: If order not found.
        ConflictException: If variant not in order, or duplicate open exchange exists.
    """
    # Validate order exists and load its items
    order_result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == data.order_id)
    )
    order = order_result.scalar_one_or_none()
    if order is None:
        raise NotFoundException(f"Order {data.order_id} not found")

    # Validate original variant belongs to this order
    order_variant_ids = {item.variant_id for item in order.items}
    if data.original_variant_id not in order_variant_ids:
        raise ConflictException(
            "The requested variant is not part of this order"
        )

    # Prevent duplicate open exchange for same order + variant
    dupe_result = await db.execute(
        select(Exchange).where(
            Exchange.order_id == data.order_id,
            Exchange.original_variant_id == data.original_variant_id,
            Exchange.status.in_(["requested", "approved", "shipped"]),
        )
    )
    if dupe_result.scalar_one_or_none() is not None:
        raise ConflictException(
            "An open exchange already exists for this order and variant"
        )

    exchange = Exchange(
        order_id=data.order_id,
        original_variant_id=data.original_variant_id,
        customer_notes=data.customer_notes,
        status="requested",
    )
    db.add(exchange)
    await db.flush()

    # Fire-and-forget email notification
    from src.core.config import get_settings
    try:
        asyncio.create_task(
            resend_client.send_exchange_notification(
                order_id=str(data.order_id),
                customer_email=order.customer_email,
                admin_email=get_settings().resend_support_email,
                exchange_details=(
                    f"Exchange requested for variant {data.original_variant_id}. "
                    f"Notes: {data.customer_notes or 'None'}"
                ),
            )
        )
    except RuntimeError:
        # No running event loop (e.g., in some test environments) — skip notification
        pass

    return exchange


async def update_exchange(
    db: AsyncSession,
    exchange_id: uuid.UUID,
    data: ExchangeAdminUpdate,
) -> Exchange:
    """Admin updates an exchange — status, replacement variant, and/or notes.

    If replacement_variant_id is provided, validates it belongs to the same
    product line as the original variant (same-line exchanges only).

    Raises:
        NotFoundException: If exchange or replacement variant not found.
        ConflictException: If replacement is a different product line.
    """
    exchange = await get_exchange(db, exchange_id)

    if data.replacement_variant_id is not None:
        # Load original and replacement variants with their products
        orig_result = await db.execute(
            select(ProductVariant)
            .options(selectinload(ProductVariant.product))
            .where(ProductVariant.id == exchange.original_variant_id)
        )
        original = orig_result.scalar_one_or_none()
        if original is None:
            raise NotFoundException(
                f"Original variant {exchange.original_variant_id} not found"
            )

        repl_result = await db.execute(
            select(ProductVariant)
            .options(selectinload(ProductVariant.product))
            .where(ProductVariant.id == data.replacement_variant_id)
        )
        replacement = repl_result.scalar_one_or_none()
        if replacement is None:
            raise NotFoundException(
                f"Replacement variant {data.replacement_variant_id} not found"
            )

        if original.product.line != replacement.product.line:
            raise ConflictException(
                f"Replacement must be the same product line "
                f"(original: {original.product.line}, "
                f"replacement: {replacement.product.line})"
            )

        exchange.replacement_variant_id = data.replacement_variant_id

    previous_status = exchange.status
    if data.status is not None:
        exchange.status = data.status

    if data.admin_notes is not None:
        exchange.admin_notes = data.admin_notes

    await db.flush()

    # Fire customer emails on key status transitions
    if data.status is not None and data.status != previous_status:
        order_result = await db.execute(
            select(Order).where(Order.id == exchange.order_id)
        )
        order = order_result.scalar_one_or_none()
        if order is not None:
            if data.status == "approved":
                await resend_client.send_exchange_approved(
                    order.customer_email, str(exchange.order_id)
                )
            elif data.status == "shipped":
                await resend_client.send_exchange_shipped(
                    order.customer_email, str(exchange.order_id)
                )

    return exchange
