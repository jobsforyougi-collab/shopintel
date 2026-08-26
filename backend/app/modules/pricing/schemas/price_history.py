from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceHistoryItem(BaseModel):
    """
    Single historical price observation returned to API consumers.

    Used by the frontend price-history graph.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: Decimal
    reference_amount: Decimal | None
    currency_code: str
    price_type: str
    availability_status: str
    captured_at: datetime


class PriceHistoryResponse(BaseModel):
    """
    Historical price series for a marketplace product.

    The frontend can use:
    - captured_at as the X-axis
    - amount as the actual price series
    - reference_amount as an optional reference-price series
    """

    marketplace_product_id: UUID
    start_at: datetime | None
    end_at: datetime | None
    count: int
    items: list[PriceHistoryItem]