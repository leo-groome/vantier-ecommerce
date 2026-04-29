"""Business logic for the inventory feature slice."""

from __future__ import annotations

import io
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import NotFoundException, StockInsufficientException
from src.features.inventory.models import OperatingCost
from src.features.inventory.schemas import OperatingCostCreate, OperatingCostUpdate, StockAdjustmentResponse
from src.features.products.models import ProductVariant
from src.integrations import resend_client

_LOW_STOCK_THRESHOLD = 50


# ── Stock management ───────────────────────────────────────────────────────────

async def adjust_stock(
    db: AsyncSession,
    variant_id: uuid.UUID,
    delta: int,
    reason: str | None = None,
) -> StockAdjustmentResponse:
    """Atomically adjust a variant's stock quantity.

    Uses SELECT FOR UPDATE to prevent race conditions when concurrent
    requests adjust the same variant simultaneously.

    Args:
        db: Async database session.
        variant_id: UUID of the variant to adjust.
        delta: Units to add (positive) or remove (negative).
        reason: Optional human-readable reason for the adjustment.

    Returns:
        StockAdjustmentResponse with new qty and low_stock_alert flag.

    Raises:
        NotFoundException: If variant does not exist.
        ConflictException: If adjustment would make stock negative.
    """
    result = await db.execute(
        select(ProductVariant)
        .where(ProductVariant.id == variant_id)
        .with_for_update()
    )
    variant = result.scalar_one_or_none()
    if variant is None:
        raise NotFoundException(f"Variant {variant_id} not found")

    new_qty = int(variant.stock_qty) + delta
    if new_qty < 0:
        raise StockInsufficientException(
            f"Stock adjustment would result in negative stock "
            f"(current: {variant.stock_qty}, delta: {delta})"
        )

    variant.stock_qty = new_qty
    await db.flush()

    is_low = new_qty <= _LOW_STOCK_THRESHOLD
    if is_low:
        await resend_client.send_low_stock_alert([
            {
                "sku": variant.sku,
                "style": variant.style,
                "size": variant.size,
                "color": variant.color,
                "stock_qty": new_qty,
            }
        ])

    return StockAdjustmentResponse(
        variant_id=variant_id,
        new_stock_qty=new_qty,
        low_stock_alert=is_low,
    )


async def get_low_stock_variants(
    db: AsyncSession,
    threshold: int = _LOW_STOCK_THRESHOLD,
) -> list[ProductVariant]:
    """Return all active variants at or below the low-stock threshold.

    Args:
        db: Async database session.
        threshold: Stock level at or below which a variant is flagged (default 50).

    Returns:
        List of ProductVariant ORM instances ordered by stock_qty ascending.
    """
    result = await db.execute(
        select(ProductVariant)
        .where(
            ProductVariant.stock_qty <= threshold,
            ProductVariant.is_active == True,  # noqa: E712
        )
        .options(selectinload(ProductVariant.images))
        .order_by(ProductVariant.stock_qty.asc())
    )
    return list(result.scalars().all())


# ── Barcode PDF generation ─────────────────────────────────────────────────────

async def generate_barcode_pdf(db: AsyncSession, variant_id: uuid.UUID) -> bytes:
    """Generate a printable PDF barcode label for a variant.

    Uses python-barcode (Code128) to render the barcode image and
    ReportLab to embed it into a PDF with the SKU printed below.

    Args:
        db: Async database session.
        variant_id: UUID of the variant.

    Returns:
        Raw PDF bytes ready for streaming to the client.

    Raises:
        NotFoundException: If variant does not exist.
    """
    import barcode  # type: ignore[import]
    from barcode.writer import ImageWriter  # type: ignore[import]
    from reportlab.lib.pagesizes import A4  # type: ignore[import]
    from reportlab.lib.units import cm  # type: ignore[import]
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate  # type: ignore[import]
    from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import]

    result = await db.execute(
        select(ProductVariant).where(ProductVariant.id == variant_id)
    )
    variant = result.scalar_one_or_none()
    if variant is None:
        raise NotFoundException(f"Variant {variant_id} not found")

    # Generate barcode PNG in memory
    barcode_buf = io.BytesIO()
    code128 = barcode.get("code128", variant.barcode, writer=ImageWriter())
    code128.write(barcode_buf, options={"write_text": False, "quiet_zone": 2})
    barcode_buf.seek(0)

    # Build PDF in memory
    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    story = [
        Image(barcode_buf, width=8 * cm, height=3 * cm),
        Paragraph(f"SKU: <b>{variant.sku}</b>", styles["Normal"]),
        Paragraph(f"{variant.style.upper()} · {variant.size} · {variant.color}", styles["Normal"]),
    ]
    doc.build(story)
    pdf_buf.seek(0)
    return pdf_buf.read()


# ── Operating Costs CRUD ───────────────────────────────────────────────────────

async def list_operating_costs(db: AsyncSession) -> list[OperatingCost]:
    """Return all operating cost entries ordered by label."""
    result = await db.execute(
        select(OperatingCost).order_by(OperatingCost.label)
    )
    return list(result.scalars().all())


async def create_operating_cost(
    db: AsyncSession, data: OperatingCostCreate
) -> OperatingCost:
    """Create a new operating cost entry.

    Args:
        db: Async database session.
        data: Validated creation payload.

    Returns:
        Newly created OperatingCost ORM instance.
    """
    cost = OperatingCost(
        label=data.label,
        amount_usd=data.amount_usd,
        is_recurring=data.is_recurring,
        notes=data.notes,
    )
    db.add(cost)
    await db.flush()
    return cost


async def update_operating_cost(
    db: AsyncSession, cost_id: uuid.UUID, data: OperatingCostUpdate
) -> OperatingCost:
    """Partially update an operating cost entry.

    Args:
        db: Async database session.
        cost_id: UUID of the entry to update.
        data: Fields to update (None fields are skipped).

    Returns:
        Updated OperatingCost ORM instance.

    Raises:
        NotFoundException: If entry does not exist.
    """
    result = await db.execute(
        select(OperatingCost).where(OperatingCost.id == cost_id)
    )
    cost = result.scalar_one_or_none()
    if cost is None:
        raise NotFoundException(f"OperatingCost {cost_id} not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(cost, field, value)
    await db.flush()
    return cost


async def delete_operating_cost(db: AsyncSession, cost_id: uuid.UUID) -> None:
    """Hard-delete an operating cost entry.

    Args:
        db: Async database session.
        cost_id: UUID of the entry to delete.

    Raises:
        NotFoundException: If entry does not exist.
    """
    result = await db.execute(
        select(OperatingCost).where(OperatingCost.id == cost_id)
    )
    cost = result.scalar_one_or_none()
    if cost is None:
        raise NotFoundException(f"OperatingCost {cost_id} not found")
    await db.delete(cost)
    await db.flush()
