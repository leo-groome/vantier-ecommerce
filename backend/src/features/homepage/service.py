"""Business logic for the homepage CMS feature slice."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.features.homepage.models import Collection, HeroSlide
from src.features.homepage.schemas import (
    CollectionCreate,
    CollectionUpdate,
    HeroSlideCreate,
    HeroSlideUpdate,
)


# ── Hero Slides ────────────────────────────────────────────────────────────────

async def list_hero_slides(db: AsyncSession, include_inactive: bool = False) -> list[HeroSlide]:
    q = select(HeroSlide).order_by(HeroSlide.position)
    if not include_inactive:
        q = q.where(HeroSlide.is_active == True)  # noqa: E712
    return list((await db.execute(q)).scalars().all())


async def get_hero_slide(db: AsyncSession, slide_id: uuid.UUID) -> HeroSlide:
    result = await db.execute(select(HeroSlide).where(HeroSlide.id == slide_id))
    slide = result.scalar_one_or_none()
    if slide is None:
        raise NotFoundException(f"HeroSlide {slide_id} not found")
    return slide


async def create_hero_slide(db: AsyncSession, data: HeroSlideCreate) -> HeroSlide:
    slide = HeroSlide(**data.model_dump())
    db.add(slide)
    await db.flush()
    await db.refresh(slide)
    return slide


async def update_hero_slide(
    db: AsyncSession, slide_id: uuid.UUID, data: HeroSlideUpdate
) -> HeroSlide:
    slide = await get_hero_slide(db, slide_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(slide, field, value)
    await db.flush()
    await db.refresh(slide)
    return slide


async def delete_hero_slide(db: AsyncSession, slide_id: uuid.UUID) -> None:
    slide = await get_hero_slide(db, slide_id)
    await db.delete(slide)
    await db.flush()


async def set_hero_slide_image(
    db: AsyncSession, slide_id: uuid.UUID, image_url: str
) -> HeroSlide:
    slide = await get_hero_slide(db, slide_id)
    slide.image_url = image_url
    await db.flush()
    await db.refresh(slide)
    return slide


# ── Collections ────────────────────────────────────────────────────────────────

async def list_collections(db: AsyncSession, include_inactive: bool = False) -> list[Collection]:
    q = select(Collection).order_by(Collection.position)
    if not include_inactive:
        q = q.where(Collection.is_active == True)  # noqa: E712
    return list((await db.execute(q)).scalars().all())


async def get_collection(db: AsyncSession, collection_id: uuid.UUID) -> Collection:
    result = await db.execute(select(Collection).where(Collection.id == collection_id))
    col = result.scalar_one_or_none()
    if col is None:
        raise NotFoundException(f"Collection {collection_id} not found")
    return col


async def create_collection(db: AsyncSession, data: CollectionCreate) -> Collection:
    col = Collection(**data.model_dump())
    db.add(col)
    await db.flush()
    await db.refresh(col)
    return col


async def update_collection(
    db: AsyncSession, collection_id: uuid.UUID, data: CollectionUpdate
) -> Collection:
    col = await get_collection(db, collection_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(col, field, value)
    await db.flush()
    await db.refresh(col)
    return col


async def delete_collection(db: AsyncSession, collection_id: uuid.UUID) -> None:
    col = await get_collection(db, collection_id)
    await db.delete(col)
    await db.flush()


async def set_collection_image(
    db: AsyncSession, collection_id: uuid.UUID, image_url: str
) -> Collection:
    col = await get_collection(db, collection_id)
    col.image_url = image_url
    await db.flush()
    await db.refresh(col)
    return col
