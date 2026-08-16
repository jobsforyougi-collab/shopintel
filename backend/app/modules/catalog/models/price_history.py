from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class PriceHistory(BaseModel):
    """
    Immutable historical price observation.

    Each meaningful price change is recorded as a new row.
    Historical records must not be overwritten during normal operation.
    """

    __tablename__ = "price_history"

    marketplace_product_id: Mapped[str] = mapped_column(
        ForeignKey(
            "marketplace_products.id",
            name="fk_price_history_marketplace_product_id",
        ),
        nullable=False,
        comment="Marketplace product whose price was observed",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        comment="Historical monetary price amount",
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="ISO 4217 currency code",
    )

    price_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="regular",
        comment="Price type such as regular, sale, or promotion",
    )

    availability_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="unknown",
        comment="Product availability status at the time of observation",
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp when the marketplace price was observed",
    )

    raw_marketplace_payload: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Raw marketplace response retained for traceability",
    )

    marketplace_product: Mapped["MarketplaceProduct"] = relationship(
        "MarketplaceProduct",
        back_populates="price_history",
    )

    def __repr__(self) -> str:
        return (
            f"<PriceHistory("
            f"marketplace_product_id='{self.marketplace_product_id}', "
            f"amount='{self.amount}', "
            f"currency='{self.currency_code}', "
            f"captured_at='{self.captured_at}')>"
        )