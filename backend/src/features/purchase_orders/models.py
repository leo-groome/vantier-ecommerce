"""SQLAlchemy ORM models for supplier purchase orders."""

import uuid
from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class PurchaseOrder(Base):
    """A purchase order sent to the garment supplier.

    Status transitions: ordered → in_transit → received.
    On 'received', stock quantities are auto-incremented by the service layer.
    """

    __tablename__ = "purchase_orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    reference_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )  # e.g. PO-2026-001
    supplier_name: Mapped[str] = mapped_column(String(200), nullable=False)
    expected_arrival_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("ordered", "in_transit", "received", name="po_status"),
        default="ordered",
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text)
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("admin_users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        "PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan",
        lazy="raise"
    )
    created_by: Mapped["AdminUser | None"] = relationship(  # type: ignore[name-defined]
        "AdminUser", lazy="raise"
    )


class PurchaseOrderItem(Base):
    """A line item within a purchase order."""

    __tablename__ = "purchase_order_items"
    __table_args__ = (
        CheckConstraint("qty_ordered > 0", name="ck_po_item_qty_ordered_positive"),
        CheckConstraint("qty_received >= 0", name="ck_po_item_qty_received_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    po_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    qty_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    qty_received: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        "PurchaseOrder", back_populates="items", lazy="raise"
    )
    variant: Mapped["ProductVariant"] = relationship(  # type: ignore[name-defined]
        "ProductVariant", lazy="raise"
    )
