from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base_model import BaseModel


class Marketplace(BaseModel):
    """
    Master data representing an e-commerce marketplace.

    Examples:
        - Daraz
        - Amazon
        - eBay
        - AliExpress
        - Noon
    """

    __tablename__ = "marketplaces"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Human-readable marketplace name",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        comment="Unique marketplace code (e.g. daraz, amazon, ebay)",
    )

    base_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Marketplace base URL",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indicates whether the marketplace is active",
    )

    def __repr__(self) -> str:
        return f"<Marketplace(name='{self.name}', code='{self.code}')>"