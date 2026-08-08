from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class MarketplaceProduct(BaseModel):
    """
    Represents a canonical product listing on a specific marketplace region.

    MarketplaceProduct contains marketplace-specific information.
    Canonical product information remains in Product.
    """

    __tablename__ = "marketplace_products"

    __table_args__ = (
        UniqueConstraint(
            "marketplace_id",
            "marketplace_region_id",
            "marketplace_product_id",
            name="uq_marketplace_products_marketplace_region_product",
        ),
    )

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        comment="Canonical product represented by this marketplace listing",
    )

    marketplace_id: Mapped[str] = mapped_column(
        ForeignKey("marketplaces.id"),
        nullable=False,
        comment="Marketplace containing this listing",
    )

    marketplace_region_id: Mapped[str] = mapped_column(
        ForeignKey("marketplace_regions.id"),
        nullable=False,
        comment="Regional storefront containing this listing",
    )

    marketplace_product_id: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="External product/listing identifier assigned by the marketplace",
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        comment="Current marketplace product URL",
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Marketplace-specific product title",
    )

    sku: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        comment="Marketplace-specific SKU",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="active",
        comment="Marketplace listing lifecycle status",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the marketplace listing is active",
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp of the last successful marketplace synchronization",
    )

    sync_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="pending",
        comment="Marketplace synchronization status",
    )

    sync_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Latest marketplace synchronization error",
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Number of synchronization retries",
    )

    raw_marketplace_payload: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Raw marketplace response retained for traceability",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="marketplace_products",
    )

    marketplace: Mapped["Marketplace"] = relationship(
        "Marketplace",
        back_populates="marketplace_products",
    )

    marketplace_region: Mapped["MarketplaceRegion"] = relationship(
        "MarketplaceRegion",
        back_populates="marketplace_products",
    )

    def __repr__(self) -> str:
        return (
            f"<MarketplaceProduct("
            f"marketplace_product_id='{self.marketplace_product_id}')>"
        )