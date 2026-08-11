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


class MarketplaceSeller(BaseModel):
    """
    Represents a seller identity on a specific marketplace region.

    Seller contains the canonical seller identity.
    MarketplaceSeller contains marketplace-specific seller information.
    """

    __tablename__ = "marketplace_sellers"

    __table_args__ = (
        UniqueConstraint(
            "marketplace_id",
            "marketplace_region_id",
            "marketplace_seller_id",
            name="uq_marketplace_sellers_marketplace_region_seller",
        ),
    )

    seller_id: Mapped[str] = mapped_column(
        ForeignKey("sellers.id"),
        nullable=False,
        comment="Canonical seller represented by this marketplace identity",
    )

    marketplace_id: Mapped[str] = mapped_column(
        ForeignKey("marketplaces.id"),
        nullable=False,
        comment="Marketplace where this seller identity exists",
    )

    marketplace_region_id: Mapped[str] = mapped_column(
        ForeignKey("marketplace_regions.id"),
        nullable=False,
        comment="Regional storefront where this seller identity exists",
    )

    marketplace_seller_id: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="External seller identifier assigned by the marketplace",
    )

    display_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Seller name displayed by the marketplace",
    )

    profile_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        comment="Marketplace seller profile URL",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="active",
        comment="Marketplace seller lifecycle status",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the marketplace seller identity is active",
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
        comment="Marketplace seller synchronization status",
    )

    sync_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Latest marketplace seller synchronization error",
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
        comment="Raw marketplace seller response retained for traceability",
    )

    seller: Mapped["Seller"] = relationship(
        "Seller",
        back_populates="marketplace_sellers",
    )

    marketplace: Mapped["Marketplace"] = relationship(
        "Marketplace",
        back_populates="marketplace_sellers",
    )

    marketplace_region: Mapped["MarketplaceRegion"] = relationship(
        "MarketplaceRegion",
        back_populates="marketplace_sellers",
    )

    marketplace_products: Mapped[list["MarketplaceProduct"]] = relationship(
        "MarketplaceProduct",
        back_populates="marketplace_seller",
    )

    def __repr__(self) -> str:
        return (
            f"<MarketplaceSeller("
            f"marketplace_seller_id='{self.marketplace_seller_id}', "
            f"display_name='{self.display_name}')>"
        )