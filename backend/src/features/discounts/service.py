"""Business logic for the discounts feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException
from src.features.discounts.models import DiscountCode
from src.features.discounts.schemas import (
    DiscountCodeCreate,
    DiscountCodeUpdate,
    DiscountValidateRequest,
    DiscountValidateResponse,
)

_MARGIN_FLOOR = Decimal("0.50")


# ── CRUD ───────────────────────────────────────────────────────────────────────

async def list_discount_codes(db: AsyncSession) -> list[DiscountCode]:
    """Return all discount codes ordered by code alphabetically."""
    result = await db.execute(select(DiscountCode).order_by(DiscountCode.code))
    return list(result.scalars().all())


async def get_discount_code(db: AsyncSession, code_id: uuid.UUID) -> DiscountCode:
    """Fetch a discount code by UUID.

    Raises:
        NotFoundException: If not found.
    """
    result = await db.execute(
        select(DiscountCode).where(DiscountCode.id == code_id)
    )
    code = result.scalar_one_or_none()
    if code is None:
        raise NotFoundException(f"DiscountCode {code_id} not found")
    return code


async def create_discount_code(
    db: AsyncSession, data: DiscountCodeCreate
) -> DiscountCode:
    """Create a new discount code.

    Enforces:
    - `percent` type value must be ≤ 100 (checked by DB constraint too).
    - Code must be unique.

    Raises:
        ConflictException: If a code with that string already exists.
    """
    existing = await db.execute(
        select(DiscountCode).where(
            func.lower(DiscountCode.code) == data.code.lower()
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ConflictException(f"Discount code '{data.code}' already exists")

    if data.type == "percent" and data.value > 100:
        raise ConflictException("Percent discount value cannot exceed 100")

    obj = DiscountCode(
        code=data.code.upper(),
        type=data.type,
        value=data.value,
        usage_limit=data.usage_limit,
        expires_at=data.expires_at,
    )
    db.add(obj)
    await db.flush()
    return obj


async def update_discount_code(
    db: AsyncSession, code_id: uuid.UUID, data: DiscountCodeUpdate
) -> DiscountCode:
    """Partially update a discount code's mutable fields.

    Raises:
        NotFoundException: If code not found.
    """
    obj = await get_discount_code(db, code_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    return obj


# ── Validation (public endpoint) ───────────────────────────────────────────────

async def validate_discount_code(
    db: AsyncSession, req: DiscountValidateRequest
) -> DiscountValidateResponse:
    """Validate a discount code and return the computed discount amount.

    Uses SELECT FOR UPDATE to atomically check the usage limit and ensure
    no concurrent request can apply the same last use simultaneously.

    NOTE: This endpoint does NOT increment usage_count. The increment
    happens in the Orders slice when the order is confirmed (Phase 2.4).

    Raises:
        NotFoundException: If code does not exist or is inactive.
        ConflictException: If code is expired or usage limit is reached.
    """
    result = await db.execute(
        select(DiscountCode)
        .where(func.upper(DiscountCode.code) == req.code.upper())
        .with_for_update()
    )
    obj = result.scalar_one_or_none()

    if obj is None or not obj.is_active:
        raise NotFoundException(f"Discount code '{req.code}' not found or inactive")

    now = datetime.now(timezone.utc)
    if obj.expires_at is not None and obj.expires_at < now:
        raise ConflictException(f"Discount code '{req.code}' has expired")

    if obj.usage_limit is not None and obj.usage_count >= obj.usage_limit:
        raise ConflictException(f"Discount code '{req.code}' usage limit reached")

    # Compute discount amount
    subtotal = req.order_subtotal_usd
    if obj.type == "percent":
        discount_amount = (subtotal * obj.value / Decimal("100")).quantize(Decimal("0.01"))
    else:  # fixed
        discount_amount = min(obj.value, subtotal)

    new_total = max(subtotal - discount_amount, Decimal("0"))

    # Margin warning: if discounted price is < 50% of original (informational only)
    # Simplified check: discount reduces subtotal below 50% of original
    margin_warning = new_total < (subtotal * _MARGIN_FLOOR)

    return DiscountValidateResponse(
        code=obj.code,
        type=obj.type,
        value=obj.value,
        discount_amount_usd=discount_amount,
        new_total_usd=new_total,
        margin_warning=margin_warning,
    )


async def increment_usage_count(
    db: AsyncSession, code_id: uuid.UUID
) -> DiscountCode:
    """Atomically increment usage_count for a discount code.

    Called by the Orders slice (Phase 2.4) when an order using this code
    is confirmed. Uses SELECT FOR UPDATE for concurrency safety.

    Raises:
        NotFoundException: If code not found.
        ConflictException: If usage limit would be exceeded.
    """
    result = await db.execute(
        select(DiscountCode)
        .where(DiscountCode.id == code_id)
        .with_for_update()
    )
    obj = result.scalar_one_or_none()
    if obj is None:
        raise NotFoundException(f"DiscountCode {code_id} not found")

    if obj.usage_limit is not None and obj.usage_count >= obj.usage_limit:
        raise ConflictException(f"Discount code '{obj.code}' usage limit reached")

    obj.usage_count += 1
    await db.flush()
    return obj
