"""Service-layer integration tests for the purchase_orders slice."""

from __future__ import annotations

import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException
from src.features.products.models import Product, ProductVariant
from src.features.purchase_orders import service
from src.features.purchase_orders.schemas import (
    POItemCreate,
    POStatusUpdate,
    PurchaseOrderCreate,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _make_variant(db: AsyncSession, stock_qty: int = 5) -> ProductVariant:
    suffix = uuid.uuid4().hex[:4].upper()
    product = Product(line="essential", name=f"Test {suffix}")
    db.add(product)
    await db.flush()

    variant = ProductVariant(
        product_id=product.id,
        style="classic",
        size="M",
        color="Black",
        sku=f"VAT-ES-CL-M-BLACK-{suffix}",
        barcode=f"BC{suffix}",
        stock_qty=stock_qty,
        cost_acquisition_usd=Decimal("40.00"),
        price_usd=Decimal("100.00"),
    )
    db.add(variant)
    await db.flush()
    return variant


def _make_po_data(variant_id: uuid.UUID, qty: int = 10) -> PurchaseOrderCreate:
    return PurchaseOrderCreate(
        reference_number=f"PO-TEST-{uuid.uuid4().hex[:6].upper()}",
        supplier_name="Test Supplier",
        items=[POItemCreate(variant_id=variant_id, qty_ordered=qty)],
    )


# ── Tests ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_purchase_order(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    data = _make_po_data(variant.id, qty=20)

    po = await service.create_purchase_order(db_session, data, admin_id=None)

    assert po.reference_number == data.reference_number
    assert po.supplier_name == "Test Supplier"
    assert po.status == "ordered"
    assert len(po.items) == 1
    assert po.items[0].qty_ordered == 20
    assert po.items[0].qty_received == 0


@pytest.mark.asyncio
async def test_create_po_invalid_variant(db_session: AsyncSession):
    data = PurchaseOrderCreate(
        reference_number="PO-INVALID-001",
        supplier_name="Supplier",
        items=[POItemCreate(variant_id=uuid.uuid4(), qty_ordered=5)],
    )
    with pytest.raises(NotFoundException):
        await service.create_purchase_order(db_session, data, admin_id=None)


@pytest.mark.asyncio
async def test_create_po_duplicate_reference(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    data = _make_po_data(variant.id)
    await service.create_purchase_order(db_session, data, admin_id=None)

    with pytest.raises(ConflictException):
        await service.create_purchase_order(db_session, data, admin_id=None)


@pytest.mark.asyncio
async def test_update_status_ordered_to_in_transit(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    po = await service.create_purchase_order(db_session, _make_po_data(variant.id), admin_id=None)

    updated = await service.update_po_status(db_session, po.id, POStatusUpdate(status="in_transit"))

    assert updated.status == "in_transit"


@pytest.mark.asyncio
async def test_update_status_received_increments_stock(db_session: AsyncSession):
    initial_stock = 5
    qty_ordered = 20
    variant = await _make_variant(db_session, stock_qty=initial_stock)
    po = await service.create_purchase_order(
        db_session, _make_po_data(variant.id, qty=qty_ordered), admin_id=None
    )

    updated = await service.update_po_status(db_session, po.id, POStatusUpdate(status="received"))

    assert updated.status == "received"
    assert updated.items[0].qty_received == qty_ordered

    # Verify stock was incremented
    from sqlalchemy import select
    from src.features.products.models import ProductVariant as PV
    result = await db_session.execute(select(PV).where(PV.id == variant.id))
    refreshed = result.scalar_one()
    assert refreshed.stock_qty == initial_stock + qty_ordered


@pytest.mark.asyncio
async def test_update_status_invalid_transition(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    po = await service.create_purchase_order(db_session, _make_po_data(variant.id), admin_id=None)
    # Transition to received first
    await service.update_po_status(db_session, po.id, POStatusUpdate(status="received"))

    # Cannot transition away from received
    with pytest.raises(ConflictException):
        await service.update_po_status(db_session, po.id, POStatusUpdate(status="ordered"))


@pytest.mark.asyncio
async def test_get_purchase_order_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.get_purchase_order(db_session, uuid.uuid4())
