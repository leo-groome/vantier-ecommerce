"""FastAPI router for the discounts feature slice."""

from __future__ import annotations

import uuid

from fastapi import APIRouter

from src.core.dependencies import AdminUserDep, DBSession, OwnerDep
from src.features.discounts import service
from src.features.discounts.schemas import (
    DiscountCodeCreate,
    DiscountCodeResponse,
    DiscountCodeUpdate,
    DiscountValidateRequest,
    DiscountValidateResponse,
)

router = APIRouter()


# ── Owner-only endpoints ───────────────────────────────────────────────────────

@router.post("", response_model=DiscountCodeResponse, status_code=201)
async def create_discount_code(
    data: DiscountCodeCreate,
    db: DBSession,
    _owner: OwnerDep,
) -> DiscountCodeResponse:
    """Create a new discount code. Requires owner role."""
    obj = await service.create_discount_code(db, data)
    return DiscountCodeResponse.model_validate(obj)


@router.patch("/{code_id}", response_model=DiscountCodeResponse)
async def update_discount_code(
    code_id: uuid.UUID,
    data: DiscountCodeUpdate,
    db: DBSession,
    _owner: OwnerDep,
) -> DiscountCodeResponse:
    """Update usage_limit, expiry, or active flag. Requires owner role."""
    obj = await service.update_discount_code(db, code_id, data)
    return DiscountCodeResponse.model_validate(obj)


# ── Admin read endpoints ───────────────────────────────────────────────────────

@router.get("", response_model=list[DiscountCodeResponse])
async def list_discount_codes(
    db: DBSession,
    _admin: AdminUserDep,
) -> list[DiscountCodeResponse]:
    """List all discount codes. Requires admin role."""
    codes = await service.list_discount_codes(db)
    return [DiscountCodeResponse.model_validate(c) for c in codes]


@router.get("/{code_id}", response_model=DiscountCodeResponse)
async def get_discount_code(
    code_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> DiscountCodeResponse:
    """Fetch a single discount code by ID. Requires admin role."""
    obj = await service.get_discount_code(db, code_id)
    return DiscountCodeResponse.model_validate(obj)


# ── Public endpoint ────────────────────────────────────────────────────────────

@router.post("/validate", response_model=DiscountValidateResponse)
async def validate_discount_code(
    req: DiscountValidateRequest,
    db: DBSession,
) -> DiscountValidateResponse:
    """Validate a discount code and compute the discount amount.

    Public endpoint — no authentication required. Does NOT increment
    usage_count (that happens when the order is confirmed in Phase 2.4).
    """
    return await service.validate_discount_code(db, req)
