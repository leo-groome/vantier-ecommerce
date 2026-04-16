"""Pydantic schemas for the users feature slice."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


AdminRole = Literal["owner", "operative"]


# ── Input schemas ──────────────────────────────────────────────────────────────

class AdminUserInvite(BaseModel):
    """Invite a new admin user."""

    email: EmailStr
    role: AdminRole


class AdminRoleUpdate(BaseModel):
    """Update role for an existing admin."""

    role: AdminRole


class SelfRegisterRequest(BaseModel):
    """Internal use only: payload to bootstrap first owner."""

    neon_auth_user_id: str
    email: EmailStr


# ── Output schemas ─────────────────────────────────────────────────────────────

class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    neon_auth_user_id: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
