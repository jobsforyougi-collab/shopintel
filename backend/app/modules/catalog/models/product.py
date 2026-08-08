from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class Product(BaseModel):
    """
    Canonical product entity.

    Product contains marketplace-independent information.
    Marketplace-specific information belongs to MarketplaceProduct.
    """

    __tablename__ = "products"

    brand_id: Mapped[str | None] = mapped_column(
        ForeignKey("brands.id"),
        nullable=True,
        comment="Canonical brand associated with the product",
    )

    category_id: Mapped[str | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        comment="Canonical category associated with the product",
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Canonical product title",
    )

    slug: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        comment="Immutable canonical product URL slug",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Canonical product description",
    )

    model_number: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        comment="Manufacturer model number",
    )

    gtin: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Global Trade Item Number such as GTIN, EAN, or UPC",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="discovered",
        comment="Product lifecycle status",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the product is active",
    )

    brand: Mapped["Brand | None"] = relationship(
        "Brand",
        back_populates="products",
    )

    category: Mapped["Category | None"] = relationship(
        "Category",
        back_populates="products",
    )

    def __repr__(self) -> str:
        return f"<Product(title='{self.title}', slug='{self.slug}')>"