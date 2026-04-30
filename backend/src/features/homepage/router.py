"""FastAPI router for homepage CMS (hero slides + collections)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.core.dependencies import AdminUserDep, DBSession
from src.core.exceptions import AppException
from src.integrations import cloudflare_client
from src.features.homepage import service
from src.features.homepage.schemas import (
    CollectionCreate,
    CollectionOut,
    CollectionUpdate,
    HeroSlideCreate,
    HeroSlideOut,
    HeroSlideUpdate,
)

router = APIRouter()

_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


# ── Public endpoints ───────────────────────────────────────────────────────────

@router.get("/hero-slides", response_model=list[HeroSlideOut])
async def list_hero_slides(db: DBSession) -> list[HeroSlideOut]:
    """Return active hero slides ordered by position. Public."""
    slides = await service.list_hero_slides(db)
    return [HeroSlideOut.model_validate(s) for s in slides]


@router.get("/collections", response_model=list[CollectionOut])
async def list_collections(db: DBSession) -> list[CollectionOut]:
    """Return active collections ordered by position. Public."""
    cols = await service.list_collections(db)
    return [CollectionOut.model_validate(c) for c in cols]


# ── Admin endpoints — hero slides ──────────────────────────────────────────────

@router.get("/admin/hero-slides", response_model=list[HeroSlideOut])
async def list_hero_slides_admin(db: DBSession, _admin: AdminUserDep) -> list[HeroSlideOut]:
    """Return all hero slides including inactive ones. Admin only."""
    slides = await service.list_hero_slides(db, include_inactive=True)
    return [HeroSlideOut.model_validate(s) for s in slides]


@router.post("/admin/hero-slides", response_model=HeroSlideOut, status_code=201)
async def create_hero_slide(
    data: HeroSlideCreate, db: DBSession, _admin: AdminUserDep
) -> HeroSlideOut:
    slide = await service.create_hero_slide(db, data)
    return HeroSlideOut.model_validate(slide)


@router.patch("/admin/hero-slides/{slide_id}", response_model=HeroSlideOut)
async def update_hero_slide(
    slide_id: uuid.UUID, data: HeroSlideUpdate, db: DBSession, _admin: AdminUserDep
) -> HeroSlideOut:
    slide = await service.update_hero_slide(db, slide_id, data)
    return HeroSlideOut.model_validate(slide)


@router.delete("/admin/hero-slides/{slide_id}", status_code=204)
async def delete_hero_slide(
    slide_id: uuid.UUID, db: DBSession, _admin: AdminUserDep
) -> None:
    await service.delete_hero_slide(db, slide_id)


@router.post("/admin/hero-slides/{slide_id}/image", response_model=HeroSlideOut)
async def upload_hero_slide_image(
    slide_id: uuid.UUID,
    file: Annotated[UploadFile, File(description="Hero slide background image")],
    db: DBSession,
    _admin: AdminUserDep,
) -> HeroSlideOut:
    """Upload background image for a hero slide to Cloudflare R2. Admin only."""
    content_type = file.content_type or "application/octet-stream"
    if content_type not in _ALLOWED_IMAGE_TYPES:
        raise AppException(f"Unsupported file type: {content_type}", status_code=422)
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise AppException("Image exceeds 10 MB size limit", status_code=413)
    url = await cloudflare_client.upload_image(
        raw, file.filename or "slide.jpg", folder=f"homepage/hero/{slide_id}"
    )
    slide = await service.set_hero_slide_image(db, slide_id, url)
    return HeroSlideOut.model_validate(slide)


# ── Admin endpoints — collections ──────────────────────────────────────────────

@router.get("/admin/collections", response_model=list[CollectionOut])
async def list_collections_admin(db: DBSession, _admin: AdminUserDep) -> list[CollectionOut]:
    """Return all collections including inactive. Admin only."""
    cols = await service.list_collections(db, include_inactive=True)
    return [CollectionOut.model_validate(c) for c in cols]


@router.post("/admin/collections", response_model=CollectionOut, status_code=201)
async def create_collection(
    data: CollectionCreate, db: DBSession, _admin: AdminUserDep
) -> CollectionOut:
    col = await service.create_collection(db, data)
    return CollectionOut.model_validate(col)


@router.patch("/admin/collections/{collection_id}", response_model=CollectionOut)
async def update_collection(
    collection_id: uuid.UUID, data: CollectionUpdate, db: DBSession, _admin: AdminUserDep
) -> CollectionOut:
    col = await service.update_collection(db, collection_id, data)
    return CollectionOut.model_validate(col)


@router.delete("/admin/collections/{collection_id}", status_code=204)
async def delete_collection(
    collection_id: uuid.UUID, db: DBSession, _admin: AdminUserDep
) -> None:
    await service.delete_collection(db, collection_id)


@router.post("/admin/collections/{collection_id}/image", response_model=CollectionOut)
async def upload_collection_image(
    collection_id: uuid.UUID,
    file: Annotated[UploadFile, File(description="Collection cover image")],
    db: DBSession,
    _admin: AdminUserDep,
) -> CollectionOut:
    """Upload cover image for a collection to Cloudflare R2. Admin only."""
    content_type = file.content_type or "application/octet-stream"
    if content_type not in _ALLOWED_IMAGE_TYPES:
        raise AppException(f"Unsupported file type: {content_type}", status_code=422)
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise AppException("Image exceeds 10 MB size limit", status_code=413)
    url = await cloudflare_client.upload_image(
        raw, file.filename or "collection.jpg", folder=f"homepage/collections/{collection_id}"
    )
    col = await service.set_collection_image(db, collection_id, url)
    return CollectionOut.model_validate(col)
