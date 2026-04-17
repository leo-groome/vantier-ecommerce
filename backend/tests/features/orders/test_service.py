"""Service-layer integration tests for the orders slice."""

from __future__ import annotations

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException, StockInsufficientException
from src.features.discounts.models import DiscountCode
from src.features.discounts.schemas import DiscountCodeCreate
from src.features.discounts import service as discounts_service
from src.features.orders import service
from src.features.orders.models import Order
from src.features.orders.schemas import OrderCreate, OrderItemCreate, ShippingAddressCreate
from src.features.products.models import Product, ProductVariant


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _make_variant(
    db: AsyncSession,
    stock_qty: int = 10,
    price: Decimal = Decimal("100.00"),
    cost: Decimal = Decimal("40.00"),
) -> ProductVariant:
    """Create a Product + ProductVariant, return the variant."""
    suffix = uuid.uuid4().hex[:4].upper()
    product = Product(line="essential", name=f"Test Product {suffix}")
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
        cost_acquisition_usd=cost,
        price_usd=price,
    )
    db.add(variant)
    await db.flush()
    return variant


def _make_order_data(
    variant_id: uuid.UUID,
    qty: int = 1,
    discount_code: str | None = None,
    email: str = "customer@test.com",
) -> OrderCreate:
    return OrderCreate(
        customer_email=email,
        customer_name="Test Customer",
        items=[OrderItemCreate(variant_id=variant_id, qty=qty)],
        shipping_address=ShippingAddressCreate(
            full_name="Test Customer",
            line1="123 Main St",
            city="Los Angeles",
            state="CA",
            zip="90001",
            country="US",
        ),
        discount_code=discount_code,
    )


async def _make_discount(
    db: AsyncSession,
    code: str = "SAVE10",
    type: str = "percent",
    value: Decimal = Decimal("10"),
    usage_limit: int | None = None,
) -> DiscountCode:
    data = DiscountCodeCreate(code=code, type=type, value=value, usage_limit=usage_limit)
    return await discounts_service.create_discount_code(db, data)


# ── create_order ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_order_success(db_session: AsyncSession):
    """Happy path: correct totals, order + items created, checkout URL returned."""
    variant = await _make_variant(db_session, stock_qty=5, price=Decimal("80.00"))
    data = _make_order_data(variant.id, qty=2)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as mock_stripe:
        mock_stripe.return_value = (f"https://checkout.stripe.mock/{uuid.uuid4()}", "cs_test_mock")
        order, checkout_url = await service.create_order(db_session, user_id=None, data=data)

    assert order.id is not None
    assert order.customer_email == "customer@test.com"
    assert order.status == "pending"
    assert order.payment_status == "pending"
    assert order.subtotal_usd == Decimal("160.00")  # 80 * 2
    assert order.is_free_shipping is False
    assert order.shipping_usd == Decimal("9.99")    # stub rate
    assert order.total_usd == Decimal("169.99")
    assert order.discount_usd == Decimal("0.00")
    assert checkout_url.startswith("https://checkout.stripe.mock/")
    mock_stripe.assert_called_once()


@pytest.mark.asyncio
async def test_create_order_guest_checkout(db_session: AsyncSession):
    """Guest checkout: user_id=None stored on order."""
    variant = await _make_variant(db_session)
    data = _make_order_data(variant.id)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/guest", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    assert order.neon_auth_user_id is None


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(db_session: AsyncSession):
    """Requesting more than available stock raises StockInsufficientException."""
    variant = await _make_variant(db_session, stock_qty=2)
    data = _make_order_data(variant.id, qty=5)

    with pytest.raises(StockInsufficientException):
        await service.create_order(db_session, user_id=None, data=data)


@pytest.mark.asyncio
async def test_create_order_free_shipping(db_session: AsyncSession):
    """5+ total items → free shipping, is_free_shipping=True, shipping_usd=0."""
    variant = await _make_variant(db_session, stock_qty=10, price=Decimal("50.00"))
    data = OrderCreate(
        customer_email="vip@test.com",
        customer_name="VIP",
        items=[OrderItemCreate(variant_id=variant.id, qty=5)],
        shipping_address=ShippingAddressCreate(
            full_name="VIP", line1="1 First St", city="LA", state="CA", zip="90002", country="US"
        ),
    )

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/free", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    assert order.is_free_shipping is True
    assert order.shipping_usd == Decimal("0.00")
    assert order.subtotal_usd == Decimal("250.00")  # 50 * 5
    assert order.total_usd == Decimal("250.00")


@pytest.mark.asyncio
async def test_create_order_with_discount(db_session: AsyncSession):
    """Valid discount code reduces total correctly."""
    variant = await _make_variant(db_session, stock_qty=5, price=Decimal("100.00"))
    await _make_discount(db_session, code="PCT10", type="percent", value=Decimal("10"))
    data = _make_order_data(variant.id, qty=1, discount_code="PCT10")

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/discount", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    assert order.discount_usd == Decimal("10.00")   # 10% of 100
    assert order.subtotal_usd == Decimal("100.00")
    # total = 100 + 9.99 (shipping) - 10 = 99.99
    assert order.total_usd == Decimal("99.99")
    assert order.discount_code_id is not None


@pytest.mark.asyncio
async def test_create_order_unknown_variant(db_session: AsyncSession):
    """Unknown variant_id raises NotFoundException."""
    data = _make_order_data(uuid.uuid4(), qty=1)

    with pytest.raises(NotFoundException):
        await service.create_order(db_session, user_id=None, data=data)


# ── confirm_payment ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_confirm_payment_decrements_stock(db_session: AsyncSession):
    """Stripe webhook: stock decremented, order marked paid/processing."""
    variant = await _make_variant(db_session, stock_qty=5, price=Decimal("100.00"))
    data = _make_order_data(variant.id, qty=3)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/order123", "cs_test_order123")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    session_id = order.stripe_checkout_session_id

    with patch("src.integrations.resend_client.send_order_confirmed", new_callable=AsyncMock):
        with patch("src.integrations.resend_client.send_new_order_alert", new_callable=AsyncMock):
            confirmed = await service.confirm_payment(db_session, session_id)

    assert confirmed is not None
    assert confirmed.payment_status == "paid"
    assert confirmed.status == "processing"

    # Verify stock was decremented
    from sqlalchemy import select
    result = await db_session.execute(
        select(ProductVariant).where(ProductVariant.id == variant.id)
    )
    refreshed = result.scalar_one()
    assert int(refreshed.stock_qty) == 2  # 5 - 3


@pytest.mark.asyncio
async def test_confirm_payment_idempotent(db_session: AsyncSession):
    """Calling confirm_payment twice for the same session does not double-decrement."""
    variant = await _make_variant(db_session, stock_qty=5, price=Decimal("100.00"))
    data = _make_order_data(variant.id, qty=2)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/idempotent", "cs_test_idempotent")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    session_id = order.stripe_checkout_session_id

    with patch("src.integrations.resend_client.send_order_confirmed", new_callable=AsyncMock):
        with patch("src.integrations.resend_client.send_new_order_alert", new_callable=AsyncMock):
            await service.confirm_payment(db_session, session_id)
            await service.confirm_payment(db_session, session_id)  # second call — idempotent

    from sqlalchemy import select
    result = await db_session.execute(
        select(ProductVariant).where(ProductVariant.id == variant.id)
    )
    refreshed = result.scalar_one()
    assert int(refreshed.stock_qty) == 3  # 5 - 2, NOT 5 - 4


@pytest.mark.asyncio
async def test_confirm_payment_fires_emails(db_session: AsyncSession):
    """Email functions are called exactly once on successful payment confirmation."""
    variant = await _make_variant(db_session, stock_qty=5, price=Decimal("50.00"))
    data = _make_order_data(variant.id, qty=1)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/emails", "cs_test_emails")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    with patch("src.integrations.resend_client.send_order_confirmed", new_callable=AsyncMock) as mock_confirmed:
        with patch("src.integrations.resend_client.send_new_order_alert", new_callable=AsyncMock) as mock_alert:
            await service.confirm_payment(db_session, order.stripe_checkout_session_id)

    mock_confirmed.assert_called_once()
    mock_alert.assert_called_once()


@pytest.mark.asyncio
async def test_confirm_payment_unknown_session_returns_none(db_session: AsyncSession):
    """Unknown session_id returns None (handles unrelated Stripe events gracefully)."""
    result = await service.confirm_payment(db_session, "cs_unknown_123")
    assert result is None


# ── update_order_status ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_status_valid_transition(db_session: AsyncSession):
    """processing → shipped is a valid transition."""
    variant = await _make_variant(db_session)
    data = _make_order_data(variant.id)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/status", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    # Manually move to processing (bypasses state machine for setup)
    order.status = "processing"
    await db_session.flush()

    with patch("src.integrations.resend_client.send_order_shipped", new_callable=AsyncMock):
        updated = await service.update_order_status(db_session, order.id, "shipped")

    assert updated.status == "shipped"


@pytest.mark.asyncio
async def test_update_status_invalid_transition(db_session: AsyncSession):
    """pending → delivered is not a valid transition."""
    variant = await _make_variant(db_session)
    data = _make_order_data(variant.id)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/invalid", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    with pytest.raises(ConflictException):
        await service.update_order_status(db_session, order.id, "delivered")


@pytest.mark.asyncio
async def test_update_status_shipped_fires_email(db_session: AsyncSession):
    """Transitioning to 'shipped' fires send_order_shipped when tracking exists."""
    variant = await _make_variant(db_session)
    data = _make_order_data(variant.id)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/shipped", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    order.status = "processing"
    order.carrier_tracking_number = "TRK123456"
    await db_session.flush()

    with patch("src.integrations.resend_client.send_order_shipped", new_callable=AsyncMock) as mock_shipped:
        await service.update_order_status(db_session, order.id, "shipped")

    mock_shipped.assert_called_once_with(
        order.customer_email, "TRK123456", carrier="envia.com"
    )


# ── generate_shipping_label ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_shipping_label(db_session: AsyncSession):
    """Shipping label generation stores tracking number and label URL on order."""
    variant = await _make_variant(db_session)
    data = _make_order_data(variant.id)

    with patch("src.integrations.stripe_client.create_checkout_session", new_callable=AsyncMock) as m:
        m.return_value = ("https://checkout.stripe.mock/label", "cs_test_mock")
        order, _ = await service.create_order(db_session, user_id=None, data=data)

    updated = await service.generate_shipping_label(db_session, order.id)

    assert updated.carrier_tracking_number is not None
    assert updated.envia_label_url is not None
    assert updated.envia_label_url.startswith("https://envia.mock/label/")
