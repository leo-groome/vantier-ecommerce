"""Business logic for the purchase_orders feature slice."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import ConflictException, NotFoundException
from src.features.products.models import ProductVariant
from src.features.purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from src.features.purchase_orders.schemas import (
    PurchaseOrderCreate,
    POStatusUpdate,
)

_VALID_TRANSITIONS: dict[str, set[str]] = {
    "ordered": {"in_transit", "received"},
    "in_transit": {"received"},
    "received": set(),  # terminal state
}


async def _load_po(db: AsyncSession, po_id: uuid.UUID) -> PurchaseOrder:
    """Load a PO with its items eagerly. Raises NotFoundException if missing."""
    result = await db.execute(
        select(PurchaseOrder)
        .options(selectinload(PurchaseOrder.items))
        .where(PurchaseOrder.id == po_id)
    )
    po = result.scalar_one_or_none()
    if po is None:
        raise NotFoundException(f"PurchaseOrder {po_id} not found")
    return po


async def list_purchase_orders(db: AsyncSession) -> list[PurchaseOrder]:
    """Return all POs ordered by creation date descending, items eager-loaded."""
    result = await db.execute(
        select(PurchaseOrder)
        .options(selectinload(PurchaseOrder.items))
        .order_by(PurchaseOrder.created_at.desc())
    )
    return list(result.scalars().all())


async def get_purchase_order(db: AsyncSession, po_id: uuid.UUID) -> PurchaseOrder:
    """Fetch a single PO with its items.

    Raises:
        NotFoundException: If not found.
    """
    return await _load_po(db, po_id)


async def create_purchase_order(
    db: AsyncSession,
    data: PurchaseOrderCreate,
    admin_id: uuid.UUID | None,
) -> PurchaseOrder:
    """Create a new purchase order with line items.

    Validates that all variant_ids exist. Enforces unique reference_number.

    Raises:
        NotFoundException: If any variant_id does not exist.
        ConflictException: If reference_number already exists.
    """
    # Check duplicate reference_number
    existing = await db.execute(
        select(PurchaseOrder).where(PurchaseOrder.reference_number == data.reference_number)
    )
    if existing.scalar_one_or_none() is not None:
        raise ConflictException(f"Reference number '{data.reference_number}' already exists")

    # Validate all variant IDs exist
    for item_data in data.items:
        result = await db.execute(
            select(ProductVariant).where(ProductVariant.id == item_data.variant_id)
        )
        if result.scalar_one_or_none() is None:
            raise NotFoundException(f"ProductVariant {item_data.variant_id} not found")

    po = PurchaseOrder(
        reference_number=data.reference_number,
        supplier_name=data.supplier_name,
        expected_arrival_date=data.expected_arrival_date,
        notes=data.notes,
        created_by_user_id=admin_id,
        status="ordered",
    )
    db.add(po)
    await db.flush()

    for item_data in data.items:
        po_item = PurchaseOrderItem(
            po_id=po.id,
            variant_id=item_data.variant_id,
            qty_ordered=item_data.qty_ordered,
            qty_received=0,
        )
        db.add(po_item)

    await db.flush()

    # Re-load with items for the response
    return await _load_po(db, po.id)


async def update_po_status(
    db: AsyncSession,
    po_id: uuid.UUID,
    data: POStatusUpdate,
) -> PurchaseOrder:
    """Transition PO to a new status.

    On transition to 'received': auto-increments stock_qty for each item
    by qty_ordered using SELECT FOR UPDATE to prevent race conditions.

    Raises:
        NotFoundException: If PO not found.
        ConflictException: If the transition is not allowed.
    """
    po = await _load_po(db, po_id)

    allowed = _VALID_TRANSITIONS.get(po.status, set())
    if data.status not in allowed:
        raise ConflictException(
            f"Cannot transition PO from '{po.status}' to '{data.status}'"
        )

    if data.status == "received":
        for item in po.items:
            result = await db.execute(
                select(ProductVariant)
                .where(ProductVariant.id == item.variant_id)
                .with_for_update()
            )
            variant = result.scalar_one()
            variant.stock_qty += item.qty_ordered
            item.qty_received = item.qty_ordered

    po.status = data.status
    await db.flush()
    return await _load_po(db, po.id)
