"""SQLAlchemy ORM models for orders and order line items."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Order(Base):
    """A customer order, from cart through fulfillment."""

    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    neon_auth_user_id: Mapped[str | None] = mapped_column(
        String, nullable=True, index=True
    )  # NULL for guest checkout
    customer_email: Mapped[str] = mapped_column(String, nullable=False)
    customer_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        Enum("pending", "processing", "shipped", "delivered", "cancelled", name="order_status"),
        default="pending",
        nullable=False,
        index=True,
    )
    payment_status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "failed", "refunded", name="payment_status"),
        default="pending",
        nullable=False,
        index=True,
    )
    subtotal_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"), nullable=False)
    discount_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"), nullable=False)
    total_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_address: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_free_shipping: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(String, index=True)
    stripe_checkout_session_id: Mapped[str | None] = mapped_column(String)
    carrier_tracking_number: Mapped[str | None] = mapped_column(String)
    envia_shipment_id: Mapped[str | None] = mapped_column(String)
    envia_label_url: Mapped[str | None] = mapped_column(Text)
    discount_code_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("discount_codes.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="raise"
    )
    discount_code: Mapped["DiscountCode | None"] = relationship(  # type: ignore[name-defined]
        "DiscountCode", lazy="raise"
    )


class OrderItem(Base):
    """A single line item within an order."""

    __tablename__ = "order_items"
    __table_args__ = (CheckConstraint("qty > 0", name="ck_order_item_qty_positive"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    qty: Mapped[int] = mapped_column(Numeric(10, 0), nullable=False)
    unit_price_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    order: Mapped["Order"] = relationship("Order", back_populates="items", lazy="raise")
    variant: Mapped["ProductVariant"] = relationship(  # type: ignore[name-defined]
        "ProductVariant", lazy="raise"
    )
