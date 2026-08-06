from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


class Category(BaseModel):
    """
    Canonical product category.

    Supports hierarchical (tree) categories.

    Example:
        Electronics
            ├── Mobile Phones
            ├── Laptops
            └── Tablets
    """

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Category name",
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        comment="Unique URL-friendly category slug",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Optional category description",
    )

    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        comment="Parent category ID",
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Depth level in category hierarchy",
    )

    is_leaf: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether this category has children",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the category is active",
    )

    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="children",
    )

    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
    )

    def __repr__(self) -> str:
        return f"<Category(name='{self.name}')>"