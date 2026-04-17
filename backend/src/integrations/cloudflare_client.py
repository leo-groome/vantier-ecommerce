"""Cloudflare R2 storage and Images transform integration."""

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
    settings = get_settings()
    return bool(
        settings.cloudflare_account_id
        and settings.r2_access_key_id
        and settings.r2_secret_access_key
        and settings.r2_bucket
    )


def _get_s3_client():
    """Return a configured boto3 S3 client pointing at Cloudflare R2."""
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.cloudflare_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key_id,
        aws_secret_access_key=settings.r2_secret_access_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


async def upload_image(
    file_bytes: bytes,
    original_filename: str,
    folder: str = "products",
) -> str:
    """Upload an image to Cloudflare R2 and return its public URL.

    Generates a unique filename to prevent collisions. Falls back to a
    placeholder URL when R2 credentials are not configured (development mode).

    Args:
        file_bytes: Raw image bytes.
        original_filename: Original filename (used to preserve the extension).
        folder: R2 path prefix (e.g. "products", "variants").

    Returns:
        Public URL of the uploaded image.

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


def get_transform_url(image_url: str, width: int | None = None, format: str = "webp") -> str:
    """Return a Cloudflare Image-transformed URL for resizing and format conversion.

    Cloudflare Images transformation is applied via the `/cdn-cgi/image/` path prefix
    on the R2 public domain. Requires "Polish" or "Image Resizing" to be enabled
    on the Cloudflare zone for the R2 custom domain.

    Args:
        image_url: The original R2 public URL.
        width: Target pixel width. If None, only format conversion is applied.
        format: Target image format (default: "webp").

    Returns:
        Transformed image URL string.

    Example:
        get_transform_url("https://pub-xxx.r2.dev/products/img.jpg", width=400)
        → "https://pub-xxx.r2.dev/cdn-cgi/image/width=400,format=webp/products/img.jpg"
    """
    settings = get_settings()
    base = settings.r2_public_url.rstrip("/")

    if not image_url.startswith(base):
        # Not an R2 URL — return as-is
        return image_url

    # Extract the object path from the URL
    object_path = image_url[len(base):].lstrip("/")

    params = f"format={format}"
    if width:
        params = f"width={width},{params}"

    return f"{base}/cdn-cgi/image/{params}/{object_path}"
