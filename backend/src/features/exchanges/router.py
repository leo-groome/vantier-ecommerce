"""FastAPI router for the exchanges feature slice."""

from __future__ import annotations

import uuid

from fastapi import APIRouter

from src.core.dependencies import AdminUserDep, CurrentUser, DBSession
from src.features.exchanges import service
from src.features.exchanges.schemas import (
    ExchangeAdminUpdate,
    ExchangeCreate,
    ExchangeResponse,
)

router = APIRouter()


@router.post("", response_model=ExchangeResponse, status_code=201)
async def create_exchange(
    data: ExchangeCreate,
    db: DBSession,
    _user: CurrentUser,
) -> ExchangeResponse:
    """Create an exchange request. Requires authenticated user."""
    obj = await service.create_exchange(db, data)
    return ExchangeResponse.model_validate(obj)


@router.get("", response_model=list[ExchangeResponse])
async def list_exchanges(
    db: DBSession,
    _admin: AdminUserDep,
) -> list[ExchangeResponse]:
    """List all exchanges. Requires admin role."""
    exchanges = await service.list_exchanges(db)
    return [ExchangeResponse.model_validate(e) for e in exchanges]


@router.get("/{exchange_id}", response_model=ExchangeResponse)
async def get_exchange(
    exchange_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> ExchangeResponse:
    """Fetch a single exchange by ID. Requires admin role."""
    obj = await service.get_exchange(db, exchange_id)
    return ExchangeResponse.model_validate(obj)


@router.patch("/{exchange_id}", response_model=ExchangeResponse)
async def update_exchange(
    exchange_id: uuid.UUID,
    data: ExchangeAdminUpdate,
    db: DBSession,
    _admin: AdminUserDep,
) -> ExchangeResponse:
    """Admin updates exchange status, replacement variant, or notes. Requires admin role."""
    obj = await service.update_exchange(db, exchange_id, data)
    return ExchangeResponse.model_validate(obj)
