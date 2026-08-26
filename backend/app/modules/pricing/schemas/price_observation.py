from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PriceObservation(BaseModel):
    """
    Normalized price observation received from a marketplace connector.

    This schema represents marketplace data after connector-level
    normalization and before pricing business logic is applied.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    marketplace_product_id: UUID = Field(
        description="Canonical marketplace product listing being observed",
    )

    amount: Decimal = Field(
        gt=Decimal("0"),
        decimal_places=2,
        max_digits=14,
        description="Actual marketplace selling price",
    )

    reference_amount: Decimal | None = Field(
        default=None,
        gt=Decimal("0"),
        decimal_places=2,
        max_digits=14,
        description=(
            "Marketplace-provided reference/original price used "
            "for discount display"
        ),
    )

    currency_code: str = Field(
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code",
    )

    price_type: str = Field(
        default="regular",
        min_length=1,
        max_length=30,
        description="Price type such as regular, sale, or promotion",
    )

    availability_status: str = Field(
        default="unknown",
        min_length=1,
        max_length=30,
        description="Marketplace product availability status",
    )

    captured_at: datetime = Field(
        description="Timestamp when the marketplace price was observed",
    )

    raw_marketplace_payload: dict | None = Field(
        default=None,
        description="Raw normalized marketplace response for traceability",
    )