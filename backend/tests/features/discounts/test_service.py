"""Service-layer integration tests for the discounts slice."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException
from src.features.discounts import service
from src.features.discounts.schemas import (
    DiscountCodeCreate,
    DiscountCodeUpdate,
    DiscountValidateRequest,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _make_code(
    db: AsyncSession,
    code: str = "SAVE10",
    type: str = "percent",
    value: Decimal = Decimal("10"),
    usage_limit: int | None = None,
    expires_at: datetime | None = None,
) -> object:
    data = DiscountCodeCreate(
        code=code, type=type, value=value,
        usage_limit=usage_limit, expires_at=expires_at,
    )
    return await service.create_discount_code(db, data)


# ── CRUD ───────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_discount_code(db_session: AsyncSession):
    obj = await _make_code(db_session, code="WELCOME20", type="percent", value=Decimal("20"))

    assert obj.id is not None
    assert obj.code == "WELCOME20"  # stored uppercase
    assert obj.type == "percent"
    assert obj.value == Decimal("20")
    assert obj.usage_count == 0
    assert obj.is_active is True


@pytest.mark.asyncio
async def test_create_discount_code_uppercase_normalization(db_session: AsyncSession):
    """Code is normalized to uppercase regardless of input casing."""
    obj = await _make_code(db_session, code="summer50")
    assert obj.code == "SUMMER50"


@pytest.mark.asyncio
async def test_create_duplicate_code_raises(db_session: AsyncSession):
    """Creating a code with the same string (case-insensitive) raises ConflictException."""
    await _make_code(db_session, code="DUPE")
    with pytest.raises(ConflictException):
        await _make_code(db_session, code="dupe")  # different casing → same code


@pytest.mark.asyncio
async def test_create_percent_over_100_raises(db_session: AsyncSession):
    """Percent discount value > 100 is rejected at service layer."""
    with pytest.raises(ConflictException):
        await _make_code(db_session, code="BAD", type="percent", value=Decimal("101"))


@pytest.mark.asyncio
async def test_create_fixed_discount(db_session: AsyncSession):
    """Fixed discount type stores value as-is (no 100% cap)."""
    obj = await _make_code(db_session, code="FIXED5", type="fixed", value=Decimal("5.00"))
    assert obj.type == "fixed"
    assert obj.value == Decimal("5.00")


@pytest.mark.asyncio
async def test_list_discount_codes(db_session: AsyncSession):
    await _make_code(db_session, code="ALPHA")
    await _make_code(db_session, code="BETA")

    codes = await service.list_discount_codes(db_session)
    names = [c.code for c in codes]
    assert "ALPHA" in names
    assert "BETA" in names


@pytest.mark.asyncio
async def test_update_discount_code(db_session: AsyncSession):
    """Updating usage_limit and is_active works correctly."""
    obj = await _make_code(db_session, code="UPDATE01")
    updated = await service.update_discount_code(
        db_session, obj.id, DiscountCodeUpdate(usage_limit=50, is_active=False)
    )
    assert updated.usage_limit == 50
    assert updated.is_active is False
    assert updated.value == obj.value  # unchanged


@pytest.mark.asyncio
async def test_update_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.update_discount_code(
            db_session, uuid.uuid4(), DiscountCodeUpdate(is_active=False)
        )


# ── validate_discount_code ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_validate_percent_discount(db_session: AsyncSession):
    """10% off $200 → $20 discount, $180 new total."""
    await _make_code(db_session, code="PCT10", type="percent", value=Decimal("10"))
    resp = await service.validate_discount_code(
        db_session, DiscountValidateRequest(code="PCT10", order_subtotal_usd=Decimal("200.00"))
    )
    assert resp.discount_amount_usd == Decimal("20.00")
    assert resp.new_total_usd == Decimal("180.00")
    assert resp.margin_warning is False


@pytest.mark.asyncio
async def test_validate_fixed_discount(db_session: AsyncSession):
    """Fixed $15 off $100 → $15 discount, $85 new total."""
    await _make_code(db_session, code="FIXED15", type="fixed", value=Decimal("15.00"))
    resp = await service.validate_discount_code(
        db_session, DiscountValidateRequest(code="FIXED15", order_subtotal_usd=Decimal("100.00"))
    )
    assert resp.discount_amount_usd == Decimal("15.00")
    assert resp.new_total_usd == Decimal("85.00")


@pytest.mark.asyncio
async def test_validate_fixed_discount_cannot_go_negative(db_session: AsyncSession):
    """Fixed discount larger than subtotal clamps new_total to 0."""
    await _make_code(db_session, code="HUGE", type="fixed", value=Decimal("500.00"))
    resp = await service.validate_discount_code(
        db_session, DiscountValidateRequest(code="HUGE", order_subtotal_usd=Decimal("50.00"))
    )
    assert resp.new_total_usd == Decimal("0")


@pytest.mark.asyncio
async def test_validate_triggers_margin_warning(db_session: AsyncSession):
    """60% discount triggers margin_warning (new_total < 50% of subtotal)."""
    await _make_code(db_session, code="BIG60", type="percent", value=Decimal("60"))
    resp = await service.validate_discount_code(
        db_session, DiscountValidateRequest(code="BIG60", order_subtotal_usd=Decimal("100.00"))
    )
    assert resp.margin_warning is True
    assert resp.new_total_usd == Decimal("40.00")


@pytest.mark.asyncio
async def test_validate_no_margin_warning_at_50_percent(db_session: AsyncSession):
    """Exactly 50% discount: new_total == 50% of subtotal → NO warning (boundary)."""
    await _make_code(db_session, code="EXACT50", type="percent", value=Decimal("50"))
    resp = await service.validate_discount_code(
        db_session, DiscountValidateRequest(code="EXACT50", order_subtotal_usd=Decimal("100.00"))
    )
    # new_total (50) is NOT < floor (50), so no warning
    assert resp.margin_warning is False


@pytest.mark.asyncio
async def test_validate_inactive_code_raises(db_session: AsyncSession):
    obj = await _make_code(db_session, code="INACTIVE")
    await service.update_discount_code(
        db_session, obj.id, DiscountCodeUpdate(is_active=False)
    )
    with pytest.raises(NotFoundException):
        await service.validate_discount_code(
            db_session, DiscountValidateRequest(code="INACTIVE", order_subtotal_usd=Decimal("100"))
        )


@pytest.mark.asyncio
async def test_validate_expired_code_raises(db_session: AsyncSession):
    past = datetime.now(timezone.utc) - timedelta(days=1)
    await _make_code(db_session, code="EXPIRED", expires_at=past)
    with pytest.raises(ConflictException):
        await service.validate_discount_code(
            db_session, DiscountValidateRequest(code="EXPIRED", order_subtotal_usd=Decimal("100"))
        )


@pytest.mark.asyncio
async def test_validate_usage_limit_reached_raises(db_session: AsyncSession):
    """Code with usage_limit=2 and usage_count already at 2 raises ConflictException."""
    from src.features.discounts.models import DiscountCode
    from sqlalchemy import select

    obj = await _make_code(db_session, code="MAXED", usage_limit=2)

    # Manually set usage_count to limit
    result = await db_session.execute(
        select(DiscountCode).where(DiscountCode.id == obj.id)
    )
    code_row = result.scalar_one()
    code_row.usage_count = 2
    await db_session.flush()

    with pytest.raises(ConflictException):
        await service.validate_discount_code(
            db_session, DiscountValidateRequest(code="MAXED", order_subtotal_usd=Decimal("100"))
        )


@pytest.mark.asyncio
async def test_validate_unknown_code_raises(db_session: AsyncSession):
    with pytest.raises(NotFoundException):
        await service.validate_discount_code(
            db_session, DiscountValidateRequest(code="GHOST", order_subtotal_usd=Decimal("100"))
        )


# ── increment_usage_count ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_increment_usage_count(db_session: AsyncSession):
    obj = await _make_code(db_session, code="INC01", usage_limit=5)
    updated = await service.increment_usage_count(db_session, obj.id)
    assert updated.usage_count == 1


@pytest.mark.asyncio
async def test_increment_usage_count_at_limit_raises(db_session: AsyncSession):
    from src.features.discounts.models import DiscountCode
    from sqlalchemy import select

    obj = await _make_code(db_session, code="ATLIMIT", usage_limit=1)
    result = await db_session.execute(
        select(DiscountCode).where(DiscountCode.id == obj.id)
    )
    code_row = result.scalar_one()
    code_row.usage_count = 1
    await db_session.flush()

    with pytest.raises(ConflictException):
        await service.increment_usage_count(db_session, obj.id)
