"""Service-layer integration tests for the exchanges slice."""

from __future__ import annotations

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException
from src.features.exchanges import service
from src.features.exchanges.schemas import ExchangeAdminUpdate, ExchangeCreate
from src.features.orders.models import Order, OrderItem
from src.features.products.models import Product, ProductVariant


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _make_variant(
    db: AsyncSession,
    line: str = "essential",
    suffix: str | None = None,
) -> ProductVariant:
    s = suffix or uuid.uuid4().hex[:4].upper()
    product = Product(line=line, name=f"Test {line} {s}")
    db.add(product)
    await db.flush()

    variant = ProductVariant(
        product_id=product.id,
        style="classic",
        size="M",
        color="Black",
        sku=f"VAT-ES-CL-M-BLACK-{s}",
        barcode=f"BC{s}",
        stock_qty=10,
        cost_acquisition_usd=Decimal("40.00"),
        price_usd=Decimal("100.00"),
    )
    db.add(variant)
    await db.flush()
    return variant


async def _make_order_with_variant(
    db: AsyncSession,
    variant: ProductVariant,
) -> Order:
    order = Order(
        customer_email="customer@test.com",
        customer_name="Test Customer",
        status="delivered",
        payment_status="paid",
        subtotal_usd=Decimal("100.00"),
        shipping_usd=Decimal("9.99"),
        discount_usd=Decimal("0.00"),
        total_usd=Decimal("109.99"),
        shipping_address={"line1": "123 Main St", "city": "LA", "country": "US"},
        is_free_shipping=False,
    )
    db.add(order)
    await db.flush()

    item = OrderItem(
        order_id=order.id,
        variant_id=variant.id,
        qty=1,
        unit_price_usd=Decimal("100.00"),
        customization_fee_usd=Decimal("0.00"),
    )
    db.add(item)
    await db.flush()
    return order


# ── Tests ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_exchange_happy_path(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    order = await _make_order_with_variant(db_session, variant)

    mock_notify = AsyncMock()
    with patch("src.integrations.resend_client.send_exchange_notification", mock_notify):
        exchange = await service.create_exchange(
            db_session,
            ExchangeCreate(
                order_id=order.id,
                original_variant_id=variant.id,
                customer_notes="Size too small",
            ),
        )

    assert exchange.order_id == order.id
    assert exchange.original_variant_id == variant.id
    assert exchange.status == "requested"
    assert exchange.customer_notes == "Size too small"
    mock_notify.assert_called_once()


@pytest.mark.asyncio
async def test_create_exchange_order_not_found(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    with pytest.raises(NotFoundException):
        await service.create_exchange(
            db_session,
            ExchangeCreate(order_id=uuid.uuid4(), original_variant_id=variant.id),
        )


@pytest.mark.asyncio
async def test_create_exchange_variant_not_in_order(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    other_variant = await _make_variant(db_session)
    order = await _make_order_with_variant(db_session, variant)

    with pytest.raises(ConflictException):
        await service.create_exchange(
            db_session,
            ExchangeCreate(order_id=order.id, original_variant_id=other_variant.id),
        )


@pytest.mark.asyncio
async def test_create_exchange_duplicate_pending(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    order = await _make_order_with_variant(db_session, variant)
    data = ExchangeCreate(order_id=order.id, original_variant_id=variant.id)

    mock_notify = AsyncMock()
    with patch("src.integrations.resend_client.send_exchange_notification", mock_notify):
        await service.create_exchange(db_session, data)
        with pytest.raises(ConflictException):
            await service.create_exchange(db_session, data)


@pytest.mark.asyncio
async def test_admin_update_exchange_status(db_session: AsyncSession):
    variant = await _make_variant(db_session)
    order = await _make_order_with_variant(db_session, variant)

    mock_notify = AsyncMock()
    with patch("src.integrations.resend_client.send_exchange_notification", mock_notify):
        exchange = await service.create_exchange(
            db_session,
            ExchangeCreate(order_id=order.id, original_variant_id=variant.id),
        )

    updated = await service.update_exchange(
        db_session,
        exchange.id,
        ExchangeAdminUpdate(status="approved", admin_notes="Approved — new stock available"),
    )

    assert updated.status == "approved"
    assert updated.admin_notes == "Approved — new stock available"


@pytest.mark.asyncio
async def test_admin_update_with_replacement_wrong_line(db_session: AsyncSession):
    variant_essential = await _make_variant(db_session, line="essential")
    variant_signature = await _make_variant(db_session, line="signature")
    order = await _make_order_with_variant(db_session, variant_essential)

    mock_notify = AsyncMock()
    with patch("src.integrations.resend_client.send_exchange_notification", mock_notify):
        exchange = await service.create_exchange(
            db_session,
            ExchangeCreate(order_id=order.id, original_variant_id=variant_essential.id),
        )

    with pytest.raises(ConflictException):
        await service.update_exchange(
            db_session,
            exchange.id,
            ExchangeAdminUpdate(
                status="approved",
                replacement_variant_id=variant_signature.id,
            ),
        )


@pytest.mark.asyncio
async def test_get_exchange_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.get_exchange(db_session, uuid.uuid4())
