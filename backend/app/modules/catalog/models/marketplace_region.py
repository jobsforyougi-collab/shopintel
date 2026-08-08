from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from app.shared.database.base_model import BaseModel


class MarketplaceRegion(BaseModel):
    """
    Represents a regional storefront or operating region
    of a marketplace.

    Examples:
        - Daraz Pakistan
        - Amazon United States
        - Amazon United Kingdom

    A marketplace can operate across multiple regions.
    """

    __tablename__ = "marketplace_regions"

    __table_args__ = (
        UniqueConstraint(
            "marketplace_id",
            "code",
            name="uq_marketplace_regions_marketplace_code",
        ),
    )

    marketplace_id: Mapped[str] = mapped_column(
        ForeignKey("marketplaces.id"),
        nullable=False,
        comment="Marketplace that owns this region",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Human-readable marketplace region name",
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Unique region code within the marketplace",
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
        comment="ISO 3166-1 alpha-2 country code",
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="ISO 4217 currency code",
    )

    locale: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Default locale for the marketplace region",
    )

    timezone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="IANA timezone identifier",
    )

    base_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Regional marketplace base URL",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the marketplace region is active",
    )

    marketplace: Mapped["Marketplace"] = relationship(
        "Marketplace",
        back_populates="regions",
    )

    marketplace_products: Mapped[list["MarketplaceProduct"]] = relationship(
        "MarketplaceProduct",
        back_populates="marketplace_region",
    )

    def __repr__(self) -> str:
        return (
            f"<MarketplaceRegion("
            f"name='{self.name}', "
            f"code='{self.code}')>"
        )