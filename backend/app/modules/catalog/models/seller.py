from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class Seller(BaseModel):
    """
    Canonical seller identity.

    Seller represents the business-level seller entity.
    Marketplace-specific seller identities belong to MarketplaceSeller.
    """

    __tablename__ = "sellers"

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Canonical seller name",
    )

    normalized_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        comment="Normalized seller name used for identity matching",
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Seller's official website",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Optional canonical seller description",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the seller is active",
    )

    marketplace_sellers: Mapped[list["MarketplaceSeller"]] = relationship(
        "MarketplaceSeller",
        back_populates="seller",
    )

    def __repr__(self) -> str:
        return f"<Seller(name='{self.name}')>"