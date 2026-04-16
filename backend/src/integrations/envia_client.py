"""Envia.com integration stubs."""

from __future__ import annotations

import logging
from decimal import Decimal

from src.core.config import get_settings
from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


async def get_shipping_rates(origin_zip: str, destination_zip: str) -> Decimal:
    """Get lowest shipping rate from envia.com.
    
    Standard package: 33x26x10 cm.
    """
    settings = get_settings()
    if settings.is_production:
        raise AppException("Envia integration missing credentials", status_code=503)
        
    logger.info(f"STUB: Getting shipping rate {origin_zip} -> {destination_zip}")
    return Decimal("9.99")


async def create_shipment(order_id: str, address_data: dict) -> tuple[str, str]:
    """Create shipment and generate label.
    
    Returns:
        Tuple of (tracking_number, label_url)
    """
    settings = get_settings()
    if settings.is_production:
        raise AppException("Envia integration missing credentials", status_code=503)
        
    logger.info(f"STUB: Creating shipment for order {order_id}")
    return ("MOCK_TRK_" + order_id[:8], "https://envia.mock/label/" + order_id)
