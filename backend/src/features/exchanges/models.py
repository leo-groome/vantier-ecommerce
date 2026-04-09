"""SQLAlchemy ORM model for product exchanges."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Exchange(Base):
    """A same-category exchange request initiated by a customer.

    No returns are accepted — only same-line exchanges. The replacement
    variant is assigned by an admin and must share the same product line
    as the original (enforced in service layer).
    """

    __tablename__ = "exchanges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    original_variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.id", ondelete="RESTRICT"),
        nullable=False,
    )
    replacement_variant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        Enum(
            "requested", "approved", "shipped", "completed", "rejected",
            name="exchange_status",
        ),
        default="requested",
        nullable=False,
        index=True,
    )
    customer_notes: Mapped[str | None] = mapped_column(Text)
    admin_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(  # type: ignore[name-defined]
        "Order", lazy="raise"
    )
    original_variant: Mapped["ProductVariant"] = relationship(  # type: ignore[name-defined]
        "ProductVariant", foreign_keys=[original_variant_id], lazy="raise"
    )
    replacement_variant: Mapped["ProductVariant | None"] = relationship(  # type: ignore[name-defined]
        "ProductVariant", foreign_keys=[replacement_variant_id], lazy="raise"
    )
