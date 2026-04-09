"""Neon Auth JWT verification using JWKS endpoint.

On first call, fetches the public key set from Neon Auth's JWKS URL and
caches it in memory. Keys are refreshed automatically on verification failure
(handles key rotation).
"""

import logging
from typing import Any

import httpx
from jose import JWTError, jwt
from jose.backends import RSAKey

from src.core.config import get_settings
from src.core.exceptions import UnauthorizedException

logger = logging.getLogger(__name__)

# Module-level JWKS cache: maps kid → public key
_jwks_cache: dict[str, Any] = {}


async def _fetch_jwks() -> None:
    """Fetch and cache JWKS from Neon Auth endpoint."""
    settings = get_settings()
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.neon_auth_jwks_url, timeout=10)
        response.raise_for_status()
        data = response.json()

    _jwks_cache.clear()
    for key_data in data.get("keys", []):
        kid = key_data.get("kid", "default")
        # Construct a concrete RSAKey so jwt.decode cannot fall back to
        # symmetric verification (protects against algorithm confusion attacks).
        _jwks_cache[kid] = RSAKey(key_data, algorithm="RS256")

    logger.info("JWKS refreshed, %d key(s) loaded", len(_jwks_cache))


async def verify_token(token: str) -> dict[str, Any]:
    """Verify a Neon Auth JWT and return its decoded claims.

    Args:
        token: Raw Bearer token string (without "Bearer " prefix).

    Returns:
        Decoded JWT payload with at minimum: ``sub`` (Neon user ID), ``email``.

    Raises:
        UnauthorizedException: If the token is invalid, expired, or cannot
            be verified against the cached JWKS.
    """
    settings = get_settings()

    if not _jwks_cache:
        await _fetch_jwks()

    # Try to decode header to pick the right key
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise UnauthorizedException("Invalid token format")

    kid = unverified_header.get("kid", "default")
    key_data = _jwks_cache.get(kid)

    if key_data is None:
        # Key not in cache — refresh once and retry
        await _fetch_jwks()
        key_data = _jwks_cache.get(kid)
        if key_data is None:
            raise UnauthorizedException("Unknown signing key")

    try:
        payload = jwt.decode(
            token,
            key_data,
            algorithms=["RS256"],
            audience=settings.neon_auth_audience,
        )
    except JWTError as exc:
        raise UnauthorizedException(f"Token verification failed: {exc}") from exc

    return payload


async def warm_jwks() -> None:
    """Public wrapper to pre-fetch JWKS during application startup."""
    await _fetch_jwks()
