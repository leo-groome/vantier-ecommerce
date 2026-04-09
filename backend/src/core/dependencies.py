"""Shared FastAPI dependency functions for auth, DB session, and RBAC."""

from collections.abc import AsyncGenerator
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import verify_token
from src.core.database import get_db
from src.core.exceptions import ForbiddenException, UnauthorizedException

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> dict[str, Any]:
    """Validate Bearer token and return decoded Neon Auth JWT claims.

    No database hit — purely JWT verification.

    Args:
        credentials: HTTP Bearer credentials from the Authorization header.

    Returns:
        Decoded JWT payload (includes ``sub``, ``email``, and any custom claims).

    Raises:
        UnauthorizedException: If no token provided or verification fails.
    """
    if credentials is None:
        raise UnauthorizedException("Authorization header required")
    return await verify_token(credentials.credentials)


async def get_admin_user(
    claims: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    """Resolve the authenticated user to an AdminUser DB row.

    Creates a new AdminUser record on first login if the Neon Auth user
    is already known to the system (e.g., pre-invited). Raises 403 if
    the user exists but is marked inactive, or does not exist at all.

    Args:
        claims: Decoded JWT payload from ``get_current_user``.
        db: Async database session.

    Returns:
        The matching :class:`AdminUser` ORM instance.

    Raises:
        ForbiddenException: If the user is not a registered admin.
    """
    # Import here to avoid circular imports at module load time
    from src.features.users.models import AdminUser

    neon_id = claims.get("sub")
    if not neon_id:
        raise ForbiddenException("Token missing subject claim")

    result = await db.execute(
        select(AdminUser).where(AdminUser.neon_auth_user_id == neon_id)
    )
    admin = result.scalar_one_or_none()

    if admin is None or not admin.is_active:
        raise ForbiddenException("User is not an authorized admin")

    return admin


async def require_owner(
    admin: Annotated[Any, Depends(get_admin_user)],
) -> Any:
    """Restrict endpoint to admin users with the 'owner' role.

    Args:
        admin: Resolved AdminUser from ``get_admin_user``.

    Returns:
        The same AdminUser if role is 'owner'.

    Raises:
        ForbiddenException: If role is not 'owner'.
    """
    if admin.role != "owner":
        raise ForbiddenException("Owner role required for this action")
    return admin


# Convenience type aliases for use in route signatures
CurrentUser = Annotated[dict[str, Any], Depends(get_current_user)]
AdminUserDep = Annotated[Any, Depends(get_admin_user)]
OwnerDep = Annotated[Any, Depends(require_owner)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
