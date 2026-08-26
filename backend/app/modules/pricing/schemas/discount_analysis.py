from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DiscountAnalysis(BaseModel):
    """
    Result of ShopIntel's discount credibility analysis.

    The analysis distinguishes between:
    - the discount advertised by the marketplace
    - the discount supported by observed historical prices
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    advertised_discount_percent: Decimal | None = None

    historical_lowest_price: Decimal | None = None

    historical_highest_price: Decimal | None = None

    historical_average_price: Decimal | None = None

    reference_price_supported: bool | None = None

    status: str

    confidence: Decimal