"""Service-layer integration tests for the inventory slice."""

from __future__ import annotations

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException, StockInsufficientException
from src.features.inventory import service
from src.features.inventory.models import OperatingCost
from src.features.inventory.schemas import OperatingCostCreate, OperatingCostUpdate
from src.features.products.models import Product, ProductVariant


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _make_variant(
    db: AsyncSession,
    stock_qty: int = 100,
    line: str = "polo_atelier",
) -> ProductVariant:
    """Insert a minimal product + variant and return the variant."""
    product = Product(line=line, name=f"Test Product {uuid.uuid4().hex[:4]}")
    db.add(product)
    await db.flush()

    suffix = uuid.uuid4().hex[:4].upper()
    sku = f"VAT-PA-CL-M-BLACK-{suffix}"
    variant = ProductVariant(
        product_id=product.id,
        style="classic",
        size="M",
        color="Black",
        sku=sku,
        barcode=sku,
        stock_qty=stock_qty,
        cost_acquisition_usd=Decimal("50.00"),
        price_usd=Decimal("120.00"),
    )
    db.add(variant)
    await db.flush()
    return variant


# ── adjust_stock ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adjust_stock_add_units(db_session: AsyncSession):
    """Positive delta increases stock correctly."""
    variant = await _make_variant(db_session, stock_qty=100)

    with patch("src.integrations.resend_client.send_low_stock_alert", new_callable=AsyncMock):
        result = await service.adjust_stock(db_session, variant.id, delta=20)

    assert result.new_stock_qty == 120
    assert result.low_stock_alert is False


@pytest.mark.asyncio
async def test_adjust_stock_remove_units(db_session: AsyncSession):
    """Negative delta decreases stock correctly."""
    variant = await _make_variant(db_session, stock_qty=100)

    with patch("src.integrations.resend_client.send_low_stock_alert", new_callable=AsyncMock):
        result = await service.adjust_stock(db_session, variant.id, delta=-30)

    assert result.new_stock_qty == 70
    assert result.low_stock_alert is False


@pytest.mark.asyncio
async def test_adjust_stock_triggers_low_stock_alert(db_session: AsyncSession):
    """Adjustment that brings qty to exactly 50 triggers the email alert."""
    variant = await _make_variant(db_session, stock_qty=60)

    mock_alert = AsyncMock()
    with patch("src.integrations.resend_client.send_low_stock_alert", mock_alert):
        result = await service.adjust_stock(db_session, variant.id, delta=-10)

    assert result.new_stock_qty == 50
    assert result.low_stock_alert is True
    mock_alert.assert_called_once()
    # Verify the payload contains the variant SKU
    call_args = mock_alert.call_args[0][0]
    assert call_args[0]["sku"] == variant.sku
    assert call_args[0]["stock_qty"] == 50


@pytest.mark.asyncio
async def test_adjust_stock_no_alert_above_threshold(db_session: AsyncSession):
    """Adjustment that leaves qty at 51 does NOT trigger alert."""
    variant = await _make_variant(db_session, stock_qty=60)

    mock_alert = AsyncMock()
    with patch("src.integrations.resend_client.send_low_stock_alert", mock_alert):
        result = await service.adjust_stock(db_session, variant.id, delta=-9)

    assert result.new_stock_qty == 51
    assert result.low_stock_alert is False
    mock_alert.assert_not_called()


@pytest.mark.asyncio
async def test_adjust_stock_below_zero_raises(db_session: AsyncSession):
    """Delta that would make stock negative raises StockInsufficientException."""
    variant = await _make_variant(db_session, stock_qty=5)

    with pytest.raises(StockInsufficientException):
        await service.adjust_stock(db_session, variant.id, delta=-10)


@pytest.mark.asyncio
async def test_adjust_stock_not_found(db_session: AsyncSession):
    """Unknown variant_id raises NotFoundException."""
    with pytest.raises(NotFoundException):
        await service.adjust_stock(db_session, uuid.uuid4(), delta=1)


# ── get_low_stock_variants ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_low_stock_variants(db_session: AsyncSession):
    """Only variants at or below threshold are returned."""
    low = await _make_variant(db_session, stock_qty=10)
    at_threshold = await _make_variant(db_session, stock_qty=50)
    above = await _make_variant(db_session, stock_qty=51)

    results = await service.get_low_stock_variants(db_session, threshold=50)
    ids = [v.id for v in results]

    assert low.id in ids
    assert at_threshold.id in ids
    assert above.id not in ids


@pytest.mark.asyncio
async def test_get_low_stock_excludes_inactive(db_session: AsyncSession):
    """Inactive variants are excluded from low-stock results."""
    variant = await _make_variant(db_session, stock_qty=5)
    variant.is_active = False
    await db_session.flush()

    results = await service.get_low_stock_variants(db_session)
    assert variant.id not in [v.id for v in results]


# ── generate_barcode_pdf ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_barcode_pdf_returns_bytes(db_session: AsyncSession):
    """PDF generation returns non-empty bytes starting with PDF magic number."""
    variant = await _make_variant(db_session)
    pdf = await service.generate_barcode_pdf(db_session, variant.id)

    assert isinstance(pdf, bytes)
    assert len(pdf) > 0
    assert pdf[:4] == b"%PDF"


@pytest.mark.asyncio
async def test_generate_barcode_pdf_not_found(db_session: AsyncSession):
    """Unknown variant_id raises NotFoundException."""
    with pytest.raises(NotFoundException):
        await service.generate_barcode_pdf(db_session, uuid.uuid4())


# ── Operating Cost CRUD ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_operating_cost(db_session: AsyncSession):
    data = OperatingCostCreate(
        label="Packaging", amount_usd=Decimal("3.50"), is_recurring=True
    )
    cost = await service.create_operating_cost(db_session, data)

    assert cost.id is not None
    assert cost.label == "Packaging"
    assert cost.amount_usd == Decimal("3.50")
    assert cost.is_recurring is True


@pytest.mark.asyncio
async def test_list_operating_costs(db_session: AsyncSession):
    await service.create_operating_cost(
        db_session, OperatingCostCreate(label="Labels", amount_usd=Decimal("1.00"))
    )
    await service.create_operating_cost(
        db_session, OperatingCostCreate(label="Commission", amount_usd=Decimal("2.00"))
    )

    costs = await service.list_operating_costs(db_session)
    labels = [c.label for c in costs]
    assert "Labels" in labels
    assert "Commission" in labels


@pytest.mark.asyncio
async def test_update_operating_cost(db_session: AsyncSession):
    cost = await service.create_operating_cost(
        db_session, OperatingCostCreate(label="Old Label", amount_usd=Decimal("5.00"))
    )
    updated = await service.update_operating_cost(
        db_session, cost.id, OperatingCostUpdate(label="New Label")
    )
    assert updated.label == "New Label"
    assert updated.amount_usd == Decimal("5.00")  # unchanged


@pytest.mark.asyncio
async def test_update_operating_cost_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.update_operating_cost(
            db_session, uuid.uuid4(), OperatingCostUpdate(label="X")
        )


@pytest.mark.asyncio
async def test_delete_operating_cost(db_session: AsyncSession):
    cost = await service.create_operating_cost(
        db_session, OperatingCostCreate(label="To Delete", amount_usd=Decimal("1.00"))
    )
    await service.delete_operating_cost(db_session, cost.id)

    from sqlalchemy import select
    result = await db_session.execute(
        select(OperatingCost).where(OperatingCost.id == cost.id)
    )
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_operating_cost_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.delete_operating_cost(db_session, uuid.uuid4())
