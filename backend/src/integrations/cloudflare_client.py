"""Cloudflare R2 storage integration for image upload and delivery.

Images are stored in a Cloudflare R2 bucket and served via the public
*.r2.dev URL. This works for development and MVP without a custom domain.

Post-MVP: once DNS is migrated to Cloudflare, add a custom domain to the
R2 bucket (CF Dashboard → R2 → Bucket → Settings → Custom Domain) and
update R2_PUBLIC_URL — image transformations via /cdn-cgi/image/ will
then work automatically.
"""

from __future__ import annotations

import asyncio
import logging
import mimetypes
import uuid
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from src.core.config import get_settings
from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


def _is_configured() -> bool:
    s = get_settings()
    return bool(s.r2_access_key_id and s.r2_secret_access_key and s.r2_bucket and s.cloudflare_account_id)


def _get_s3_client():
    s = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=f"https://{s.cloudflare_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=s.r2_access_key_id,
        aws_secret_access_key=s.r2_secret_access_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


async def upload_image(
    file_bytes: bytes,
    original_filename: str,
    folder: str = "products",
) -> str:
    """Upload an image to Cloudflare R2 and return its public URL.

    Args:
        file_bytes: Raw image bytes.
        original_filename: Original filename (used to preserve the extension).
        folder: R2 path prefix (e.g. "products", "variants").

    Returns:
        Public URL of the uploaded image (*.r2.dev/...).

    Raises:
        AppException: If R2 credentials are configured but the upload fails.
    """
    if not _is_configured():
        logger.info("STUB: R2 upload skipped — credentials not configured")
        return f"https://placehold.co/800x800?text={original_filename}"

    settings = get_settings()
    ext = Path(original_filename).suffix.lower() or ".jpg"
    object_key = f"{folder}/{uuid.uuid4().hex}{ext}"
    content_type = mimetypes.guess_type(original_filename)[0] or "image/jpeg"

    def _upload() -> None:
        s3 = _get_s3_client()
        s3.put_object(
            Bucket=settings.r2_bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
            CacheControl="public, max-age=31536000, immutable",
        )

    try:
        await asyncio.to_thread(_upload)
    except (BotoCoreError, ClientError) as exc:
        logger.error("R2 upload failed for %s: %s", object_key, exc)
        raise AppException(f"Image upload failed: {exc}", status_code=502) from exc

    public_url = f"{settings.r2_public_url.rstrip('/')}/{object_key}"
    logger.info("R2 upload success: %s", public_url)
    return public_url


async def delete_image(object_key: str) -> None:
    """Delete an object from R2 by its key. No-op if R2 not configured.

    Args:
        object_key: The R2 object key (path after the bucket, e.g. "products/abc.jpg").
    """
    if not _is_configured():
        return

    settings = get_settings()

    def _delete() -> None:
        s3 = _get_s3_client()
        s3.delete_object(Bucket=settings.r2_bucket, Key=object_key)

    try:
        await asyncio.to_thread(_delete)
    except (BotoCoreError, ClientError) as exc:
        logger.warning("R2 delete failed for %s: %s", object_key, exc)
