"""Neon Auth JWT verification using JWKS endpoint.

On first call, fetches the public key set from Neon Auth's JWKS URL and
caches it in memory. Keys are refreshed automatically on verification failure
(handles key rotation).

Neon Auth uses EdDSA (Ed25519 / OKP key type) — PyJWT is used instead of
python-jose because jose 3.x does not support OKP keys.

DEV BYPASS:
  Only active when ENABLE_DEV_AUTH=true is set in the environment.
  This var must NEVER be set in production or staging. It is intended
  exclusively for local pytest runs that do not hit external services.
"""

import base64
import logging
import os
from typing import Any

import httpx
import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from src.core.config import get_settings
from src.core.exceptions import UnauthorizedException

# Guard: read once at module load. Requires explicit opt-in; not toggled by ENVIRONMENT.
_DEV_AUTH_ENABLED = os.getenv("ENABLE_DEV_AUTH", "false").lower() == "true"

logger = logging.getLogger(__name__)

# Module-level JWKS cache: maps kid → public key object (Ed25519PublicKey or RSAPublicKey)
_jwks_cache: dict[str, Any] = {}


def _load_jwk(key_data: dict[str, Any]) -> Any:
    """Convert a JWK dict to a cryptography public key object.

    Args:
        key_data: A single JWK entry from the JWKS endpoint.

    Returns:
        A cryptography public key suitable for jwt.decode().

    Raises:
        ValueError: If the key type is unsupported.
    """
    kty = key_data.get("kty")

    if kty == "OKP":
        # Ed25519 — base64url-decode the 'x' coordinate
        x_bytes = base64.urlsafe_b64decode(key_data["x"] + "==")
        return Ed25519PublicKey.from_public_bytes(x_bytes)

    if kty == "RSA":
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        from jwt.algorithms import RSAAlgorithm

        return RSAAlgorithm.from_jwk(key_data)

    raise ValueError(f"Unsupported JWK key type: {kty!r}")


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
        try:
            _jwks_cache[kid] = _load_jwk(key_data)
        except (ValueError, KeyError) as exc:
            logger.warning("Skipping unsupported JWK kid=%s: %s", kid, exc)

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

    # ---- DEV BYPASS (pytest only) ----
    # Requires ENABLE_DEV_AUTH=true in env. Never expose in production/staging.
    if _DEV_AUTH_ENABLED and token.startswith("dev_token_"):
        if settings.is_production:
            raise UnauthorizedException("Dev bypass forbidden in production")
        neon_id = token.replace("dev_token_", "")
        logger.warning("DEV AUTH BYPASS used for neon_id=%s — not for production use", neon_id)
        return {"sub": neon_id, "email": "dev@vantier.com"}
    # -----------------------------------

    if not _jwks_cache:
        await _fetch_jwks()

    # Decode header without verification to pick the right cached key
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.exceptions.DecodeError:
        raise UnauthorizedException("Invalid token format")

    kid = unverified_header.get("kid", "default")
    alg = unverified_header.get("alg", "EdDSA")
    pub_key = _jwks_cache.get(kid)

    if pub_key is None:
        # Key not in cache — refresh once and retry (handles key rotation)
        await _fetch_jwks()
        pub_key = _jwks_cache.get(kid)
        if pub_key is None:
            raise UnauthorizedException("Unknown signing key")

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            pub_key,
            algorithms=[alg],
            audience=settings.neon_auth_audience,
        )
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidAudienceError:
        raise UnauthorizedException("Invalid token audience")
    except jwt.PyJWTError as exc:
        raise UnauthorizedException(f"Token verification failed: {exc}") from exc

    return payload


async def warm_jwks() -> None:
    """Public wrapper to pre-fetch JWKS during application startup."""
    await _fetch_jwks()
