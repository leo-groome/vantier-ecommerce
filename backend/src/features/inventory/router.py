"""FastAPI router for the inventory feature slice."""

from __future__ import annotations

import uuid

from fastapi import APIRouter
from fastapi.responses import Response

from src.core.dependencies import AdminUserDep, DBSession, OwnerDep
from src.features.inventory import service
from src.features.inventory.schemas import (
    OperatingCostCreate,
    OperatingCostResponse,
    OperatingCostUpdate,
    StockAdjustment,
    StockAdjustmentResponse,
)
from src.features.products.schemas import VariantResponse


router = APIRouter()


# ── Stock endpoints ────────────────────────────────────────────────────────────

@router.patch("/variants/{variant_id}/stock", response_model=StockAdjustmentResponse)
async def adjust_stock(
    variant_id: uuid.UUID,
    data: StockAdjustment,
    db: DBSession,
    _admin: AdminUserDep,
) -> StockAdjustmentResponse:
    """Adjust stock quantity for a variant (positive = add, negative = remove).

    Requires admin role. Uses SELECT FOR UPDATE to prevent race conditions.
    Triggers a low-stock email alert when new qty ≤ 50.
    """
    return await service.adjust_stock(db, variant_id, data.delta, data.reason)


@router.get("/low-stock", response_model=list[VariantResponse])
async def list_low_stock_variants(
    db: DBSession,
    _admin: AdminUserDep,
    threshold: int = 50,
) -> list[VariantResponse]:
    """List all active variants at or below the low-stock threshold.

    Requires admin role. Default threshold is 50 units per variant.
    """
    variants = await service.get_low_stock_variants(db, threshold)
    return [VariantResponse.model_validate(v) for v in variants]


@router.get("/variants/{variant_id}/barcode")
async def get_variant_barcode(
    variant_id: uuid.UUID,
    db: DBSession,
    _admin: AdminUserDep,
) -> Response:
    """Generate and download a PDF barcode label for a variant.

    Returns a PDF file as an attachment. Requires admin role.
    """
    pdf_bytes = await service.generate_barcode_pdf(db, variant_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=barcode-{variant_id}.pdf"},
    )


# ── Operating Costs endpoints ──────────────────────────────────────────────────

@router.get("/operating-costs", response_model=list[OperatingCostResponse])
async def list_operating_costs(
    db: DBSession,
    _admin: AdminUserDep,
) -> list[OperatingCostResponse]:
    """List all operating cost entries. Requires admin role."""
    costs = await service.list_operating_costs(db)
    return [OperatingCostResponse.model_validate(c) for c in costs]


@router.post("/operating-costs", response_model=OperatingCostResponse, status_code=201)
async def create_operating_cost(
    data: OperatingCostCreate,
    db: DBSession,
    _owner: OwnerDep,
) -> OperatingCostResponse:
    """Create a new operating cost entry. Requires owner role."""
    cost = await service.create_operating_cost(db, data)
    return OperatingCostResponse.model_validate(cost)


@router.patch("/operating-costs/{cost_id}", response_model=OperatingCostResponse)
async def update_operating_cost(
    cost_id: uuid.UUID,
    data: OperatingCostUpdate,
    db: DBSession,
    _owner: OwnerDep,
) -> OperatingCostResponse:
    """Partially update an operating cost entry. Requires owner role."""
    cost = await service.update_operating_cost(db, cost_id, data)
    return OperatingCostResponse.model_validate(cost)


@router.delete("/operating-costs/{cost_id}", status_code=204)
async def delete_operating_cost(
    cost_id: uuid.UUID,
    db: DBSession,
    _owner: OwnerDep,
) -> None:
    """Hard-delete an operating cost entry. Requires owner role."""
    await service.delete_operating_cost(db, cost_id)
