"""Pydantic schemas for the homepage CMS feature slice."""

from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict


# ── Hero Slides ────────────────────────────────────────────────────────────────

class HeroSlideCreate(BaseModel):
    label: str
    title: str
    subtitle: str | None = None
    cta_text: str = "Explore the Collection"
    cta_url: str = "/shop"
    theme: Literal["dark", "light"] = "dark"
    position: int = 0
    is_active: bool = True


class HeroSlideUpdate(BaseModel):
    label: str | None = None
    title: str | None = None
    subtitle: str | None = None
    cta_text: str | None = None
    cta_url: str | None = None
    theme: Literal["dark", "light"] | None = None
    position: int | None = None
    is_active: bool | None = None


class HeroSlideOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    label: str
    title: str
    subtitle: str | None
    cta_text: str
    cta_url: str
    image_url: str | None
    theme: str
    position: int
    is_active: bool


# ── Collections ────────────────────────────────────────────────────────────────

class CollectionCreate(BaseModel):
    name: str
    tagline: str | None = None
    label: str | None = None
    price_from: str | None = None
    link_url: str = "/shop"
    position: int = 0
    is_active: bool = True


class CollectionUpdate(BaseModel):
    name: str | None = None
    tagline: str | None = None
    label: str | None = None
    price_from: str | None = None
    link_url: str | None = None
    position: int | None = None
    is_active: bool | None = None


class CollectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    tagline: str | None
    label: str | None
    price_from: str | None
    link_url: str
    image_url: str | None
    position: int
    is_active: bool
