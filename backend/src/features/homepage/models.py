"""SQLAlchemy ORM models for homepage CMS (hero slides + collections)."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class HeroSlide(Base):
    """A carousel slide shown in the homepage hero section."""

    __tablename__ = "hero_slides"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(300))
    cta_text: Mapped[str] = mapped_column(String(100), nullable=False, default="Explore the Collection")
    cta_url: Mapped[str] = mapped_column(String(500), nullable=False, default="/shop")
    image_url: Mapped[str | None] = mapped_column(Text)
    theme: Mapped[str] = mapped_column(String(10), nullable=False, default="dark")  # dark | light
    position: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Collection(Base):
    """A curated product collection shown in the homepage grid."""

    __tablename__ = "collections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    tagline: Mapped[str | None] = mapped_column(String(300))
    label: Mapped[str | None] = mapped_column(String(100))
    price_from: Mapped[str | None] = mapped_column(String(50))  # e.g. "From $180"
    link_url: Mapped[str] = mapped_column(String(500), nullable=False, default="/shop")
    image_url: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
