from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class CurrentPrice(BaseModel):
    """
    Represents the latest known price for a marketplace product.

    CurrentPrice is a mutable snapshot.

    Historical price changes are stored separately in PriceHistory.
    """

    __tablename__ = "current_prices"

    __table_args__ = (
        UniqueConstraint(
            "marketplace_product_id",
            name="uq_current_prices_marketplace_product",
        ),
    )

    marketplace_product_id: Mapped[str] = mapped_column(
        ForeignKey("marketplace_products.id"),
        nullable=False,
        comment="Marketplace product whose current price is represented",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        comment="Current monetary price amount",
    )

    reference_amount: Mapped[Decimal | None] = mapped_column(
    Numeric(14, 2),
    nullable=True,
    comment="Marketplace-provided reference or original price used for discount display",
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
        comment="Current product availability status",
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp when the current price was observed",
    )

    marketplace_product: Mapped["MarketplaceProduct"] = relationship(
        "MarketplaceProduct",
        back_populates="current_price",
    )

    def __repr__(self) -> str:
        return (
            f"<CurrentPrice("
            f"marketplace_product_id='{self.marketplace_product_id}', "
            f"amount='{self.amount}', "
            f"currency='{self.currency_code}')>"
        )