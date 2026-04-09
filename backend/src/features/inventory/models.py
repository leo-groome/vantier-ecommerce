"""SQLAlchemy ORM models for operating costs and saved customer addresses."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, Index, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import true

from src.core.database import Base


class OperatingCost(Base):
    """Baseline per-order cost inputs for profitability calculations.

    Recurring costs (packaging, labels, commission) are summed and applied
    in the margin formula: (price - COGS - sum(operating_costs)) / price >= 0.50
    """

    __tablename__ = "operating_costs"
    __table_args__ = (
        CheckConstraint("amount_usd > 0", name="ck_op_cost_amount_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    amount_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SavedAddress(Base):
    """Saved shipping addresses for authenticated storefront customers.

    Keyed by Neon Auth user ID; no FK constraint since storefront customers
    are not stored in admin_users.
    """

    __tablename__ = "saved_addresses"
    __table_args__ = (
        # Only one default address per user allowed (partial unique index)
        Index(
            "uq_saved_address_default_per_user",
            "neon_auth_user_id",
            unique=True,
            postgresql_where=true(),  # replaced with is_default=true at migration time
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    neon_auth_user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    label: Mapped[str | None] = mapped_column(String(100))  # e.g. "Home"
    full_name: Mapped[str | None] = mapped_column(String(255))
    line1: Mapped[str] = mapped_column(String(255), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str | None] = mapped_column(String(100))
    zip: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)  # ISO 3166-1 alpha-2
    phone: Mapped[str | None] = mapped_column(String(30))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
