"""API endpoints for the users feature slice."""

import uuid

from fastapi import APIRouter, status

from src.core.dependencies import AdminUserDep, DBSession, OwnerDep
from src.features.users import service
from src.features.users.schemas import (
    AdminRoleUpdate,
    AdminUserInvite,
    AdminUserResponse,
)

router = APIRouter()


@router.get("/me", response_model=AdminUserResponse)
async def get_my_profile(
    admin: AdminUserDep,
) -> AdminUserResponse:
    """Return the current admin user's profile and role."""
    return admin


@router.get("", response_model=list[AdminUserResponse])
async def list_users(
    db: DBSession,
    _: OwnerDep,
) -> list[AdminUserResponse]:
    """List all active admin users (Owner only)."""
    return await service.list_admins(db)


@router.post("", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/invite", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def invite_user(
    data: AdminUserInvite,
    db: DBSession,
    _: OwnerDep,
) -> AdminUserResponse:
    """Provision a new admin user in the system (Owner only)."""
    return await service.invite_admin(db, data)


@router.patch("/{user_id}", response_model=AdminUserResponse)
async def update_user_role(
    user_id: uuid.UUID,
    data: AdminRoleUpdate,
    db: DBSession,
    _: OwnerDep,
) -> AdminUserResponse:
    """Update role for an admin user (Owner only)."""
    return await service.update_role(db, user_id, data)


@router.delete("/{user_id}", response_model=AdminUserResponse)
async def deactivate_user(
    user_id: uuid.UUID,
    db: DBSession,
    owner_user: OwnerDep,
) -> AdminUserResponse:
    """Soft-delete an admin user (Owner only). Cannot deactivate self."""
    return await service.deactivate_admin(db, user_id, current_user_id=owner_user.id)
