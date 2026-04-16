"""Business logic for the users feature slice."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppException, ConflictException, ForbiddenException, NotFoundException
from src.features.users.models import AdminUser
from src.features.users.schemas import AdminRoleUpdate, AdminUserInvite, SelfRegisterRequest


async def list_admins(db: AsyncSession) -> list[AdminUser]:
    """Return all active admin users."""
    result = await db.execute(
        select(AdminUser).where(AdminUser.is_active.is_(True)).order_by(AdminUser.created_at)
    )
    return list(result.scalars().all())


async def invite_admin(db: AsyncSession, data: AdminUserInvite) -> AdminUser:
    """Create a new admin user invite (requires pre-registration in Neon Auth).
    
    In a real system, this might send an invite email. Here, we just provision
    the DB row, expecting the user to log in via Neon Auth with matching email.
    """
    existing = await db.execute(
        select(AdminUser).where(func.lower(AdminUser.email) == data.email.lower())
    )
    if existing.scalar_one_or_none() is not None:
        raise ConflictException(f"Admin with email '{data.email}' already exists.")
    
    # Placeholder identity. True linkage happens when Neon Auth returns matching email payload
    # For now, we seed neon_auth_user_id with a placeholder that gets updated on first login,
    # or you require the operario to register FIRST and you enter their exact string ID here.
    # To keep Auth flow simple per PRD, we just use a temporary ID here.
    obj = AdminUser(
        neon_auth_user_id=f"pending_{uuid.uuid4()}",
        email=data.email,
        role=data.role
    )
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_role(
    db: AsyncSession, admin_id: uuid.UUID, data: AdminRoleUpdate
) -> AdminUser:
    """Update role for an admin user."""
    result = await db.execute(select(AdminUser).where(AdminUser.id == admin_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise NotFoundException(f"AdminUser {admin_id} not found")
        
    obj.role = data.role
    await db.flush()
    await db.refresh(obj)
    return obj


async def deactivate_admin(
    db: AsyncSession, admin_id: uuid.UUID, current_user_id: uuid.UUID
) -> AdminUser:
    """Soft-delete an admin user. Prevents self-deactivation."""
    if admin_id == current_user_id:
        raise AppException("Cannot deactivate your own account")
        
    result = await db.execute(select(AdminUser).where(AdminUser.id == admin_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise NotFoundException(f"AdminUser {admin_id} not found")
        
    obj.is_active = False
    await db.flush()
    await db.refresh(obj)
    return obj


async def get_or_create_on_login(
    db: AsyncSession, req: SelfRegisterRequest
) -> AdminUser:
    """Bootstrap function: Create first owner IF table is empty.
    
    WARNING: Only use internally (via seed script).
    """
    # Guard: Count rows
    count_res = await db.execute(select(func.count(AdminUser.id)))
    count = count_res.scalar_one()
    
    if count > 0:
        raise ForbiddenException("Admin table is not empty. Cannot auto-bootstrap owner.")
        
    obj = AdminUser(
        neon_auth_user_id=req.neon_auth_user_id,
        email=req.email,
        role="owner"
    )
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj
