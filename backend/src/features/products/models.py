"""SQLAlchemy ORM models for products, variants, and images."""

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
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Product(Base):
    """Top-level product line. Variants (size/style/color) are children."""

    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    line: Mapped[str] = mapped_column(
        Enum("polo_atelier", "signature", "essential", name="product_line"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan", lazy="raise"
    )


class ProductVariant(Base):
    """A purchasable unit: Product × Style × Size × Color."""

    __tablename__ = "product_variants"
    __table_args__ = (
        CheckConstraint("stock_qty >= 0", name="ck_variant_stock_non_negative"),
        CheckConstraint("cost_acquisition_usd >= 0", name="ck_variant_cost_non_negative"),
        CheckConstraint("price_usd > 0", name="ck_variant_price_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    style: Mapped[str] = mapped_column(
        Enum("classic", "design", name="product_style"), nullable=False
    )
    size: Mapped[str] = mapped_column(
        Enum("S", "M", "L", "XL", "XXL", "XXXL", name="product_size"), nullable=False
    )
    color: Mapped[str] = mapped_column(String(100), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    stock_qty: Mapped[int] = mapped_column(Numeric(10, 0), default=0, nullable=False)
    cost_acquisition_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="variants", lazy="raise")
    images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage", back_populates="variant", cascade="all, delete-orphan",
        order_by="ProductImage.position", lazy="raise"
    )


class ProductImage(Base):
    """Ordered image gallery for a product variant."""

    __tablename__ = "product_images"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    variant: Mapped["ProductVariant"] = relationship(
        "ProductVariant", back_populates="images", lazy="raise"
    )
