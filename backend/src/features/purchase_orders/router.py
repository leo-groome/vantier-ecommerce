"""FastAPI router for the purchase_orders feature slice."""

from __future__ import annotations

import uuid

from fastapi import APIRouter

from src.core.dependencies import AdminUserDep, DBSession
from src.features.purchase_orders import service
from src.features.purchase_orders.schemas import (
    POStatusUpdate,
    PurchaseOrderCreate,
    PurchaseOrderResponse,
)

router = APIRouter()


@router.post("", response_model=PurchaseOrderResponse, status_code=201)
async def create_purchase_order(
    data: PurchaseOrderCreate,
    db: DBSession,
    admin: AdminUserDep,
) -> PurchaseOrderResponse:
    """Create a new purchase order. Requires admin role."""
    po = await service.create_purchase_order(db, data, admin_id=admin.id)
    return PurchaseOrderResponse.model_validate(po)


@router.get("", response_model=list[PurchaseOrderResponse])
async def list_purchase_orders(
    db: DBSession,
    _admin: AdminUserDep,
) -> list[PurchaseOrderResponse]:
    """List all purchase orders, newest first. Requires admin role."""
    pos = await service.list_purchase_orders(db)
    return [PurchaseOrderResponse.model_validate(p) for p in pos]


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
async def get_purchase_order(
    po_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> PurchaseOrderResponse:
    """Fetch a single purchase order by ID. Requires admin role."""
    po = await service.get_purchase_order(db, po_id)
    return PurchaseOrderResponse.model_validate(po)


@router.patch("/{po_id}/status", response_model=PurchaseOrderResponse)
async def update_po_status(
    po_id: uuid.UUID,
    data: POStatusUpdate,
    db: DBSession,
    _admin: AdminUserDep,
) -> PurchaseOrderResponse:
    """Transition a PO status. On 'received', auto-increments stock. Requires admin role."""
    po = await service.update_po_status(db, po_id, data)
    return PurchaseOrderResponse.model_validate(po)
