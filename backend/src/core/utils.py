"""Shared utility functions: SKU generation, pagination, UUID helpers."""

import uuid
from dataclasses import dataclass

# Product line abbreviations used in SKU generation
_LINE_ABBR = {
    "polo_atelier": "PA",
    "signature": "SG",
    "essential": "ES",
}

_STYLE_ABBR = {
    "classic": "CL",
    "design": "DS",
}


def generate_sku(
    line: str,
    style: str,
    size: str,
    color: str,
) -> str:
    """Generate a unique SKU for a product variant.

    Format: ``VAT-{LINE}-{STYLE}-{SIZE}-{COLOR}-{SUFFIX}``

    Example: ``VAT-PA-CL-M-BLACK-A3F2``

    The suffix is a 4-character hex token derived from a UUID, making the
    SKU globally unique without requiring a database round-trip and without
    any race conditions under concurrent requests. The ``UNIQUE`` constraint
    on the ``sku`` column remains the authoritative uniqueness guard.

    Args:
        line: Product line enum value (e.g. ``polo_atelier``).
        style: Style enum value (e.g. ``classic``).
        size: Size enum value (e.g. ``M``).
        color: Color string (uppercased, spaces replaced with hyphens).

    Returns:
        Unique SKU string.
    """
    line_code = _LINE_ABBR.get(line, line[:2].upper())
    style_code = _STYLE_ABBR.get(style, style[:2].upper())
    color_code = color.upper().replace(" ", "-")[:10]
    size_code = size.upper()
    suffix = uuid.uuid4().hex[:4].upper()

    return f"VAT-{line_code}-{style_code}-{size_code}-{color_code}-{suffix}"


def generate_barcode_value(sku: str) -> str:
    """Derive a barcode string from a SKU.

    Uses the SKU directly as the barcode value (Code128 compatible).
    The actual barcode image is rendered by the inventory service.

    Args:
        sku: The variant's unique SKU string.

    Returns:
        Barcode string value (same as SKU for Code128).
    """
    return sku


def new_uuid() -> uuid.UUID:
    """Generate a new UUID v4."""
    return uuid.uuid4()


@dataclass
class PaginationParams:
    """Common pagination parameters for list endpoints."""

    page: int = 1
    page_size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


def paginate(page: int = 1, page_size: int = 20) -> PaginationParams:
    """FastAPI dependency for pagination query parameters."""
    page = max(1, page)
    page_size = min(max(1, page_size), 100)
    return PaginationParams(page=page, page_size=page_size)
