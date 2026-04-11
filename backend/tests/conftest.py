"""Shared pytest fixtures for Vantier backend tests."""

from collections.abc import AsyncGenerator
from datetime import datetime, timezone
import uuid

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db, get_engine
from src.core.dependencies import get_admin_user, require_owner
from src.features.users.models import AdminUser
from src.main import app


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a session whose changes are rolled back after each test."""
    engine = get_engine()
    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False, autoflush=False)
    yield session

    try:
        await session.close()
    finally:
        await transaction.rollback()
        await connection.close()


def _make_admin(role: str = "operative") -> AdminUser:
    admin = AdminUser(
        id=uuid.uuid4(),
        neon_auth_user_id=f"test-{role}-id",
        email=f"{role}@test.com",
        role=role,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return admin


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Unauthenticated HTTP client (public endpoints)."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client authenticated as an operative admin."""
    async def override_get_db():
        yield db_session

    async def override_get_admin_user():
        return _make_admin("operative")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_admin_user] = override_get_admin_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def owner_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client authenticated as the owner."""
    async def override_get_db():
        yield db_session

    async def override_get_admin_user():
        return _make_admin("owner")

    async def override_require_owner():
        return _make_admin("owner")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_admin_user] = override_get_admin_user
    app.dependency_overrides[require_owner] = override_require_owner
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
