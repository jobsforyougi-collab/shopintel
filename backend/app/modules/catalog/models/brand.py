from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Brand(BaseModel):
    """
    Canonical product brand.

    Examples:
        - Apple
        - Samsung
        - Sony
        - Nike
    """

    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        comment="Official brand name",
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        comment="URL-friendly unique brand identifier",
    )

    logo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Brand logo URL",
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Official brand website",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the brand is active",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="brand",
    )

    def __repr__(self) -> str:
        return f"<Brand(name='{self.name}')>"