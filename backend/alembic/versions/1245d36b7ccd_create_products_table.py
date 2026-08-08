"""create products table

Revision ID: 1245d36b7ccd
Revises: 2b6a4af4b00c
Create Date: 2026-08-08 13:36:35.287656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1245d36b7ccd"
down_revision: Union[str, Sequence[str], None] = "2b6a4af4b00c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "products",

        sa.Column(
            "brand_id",
            sa.UUID(),
            nullable=True,
            comment="Canonical brand associated with the product",
        ),

        sa.Column(
            "category_id",
            sa.UUID(),
            nullable=True,
            comment="Canonical category associated with the product",
        ),

        sa.Column(
            "title",
            sa.String(length=500),
            nullable=False,
            comment="Canonical product title",
        ),

        sa.Column(
            "slug",
            sa.String(length=500),
            nullable=False,
            comment="Immutable canonical product URL slug",
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Canonical product description",
        ),

        sa.Column(
            "model_number",
            sa.String(length=150),
            nullable=True,
            comment="Manufacturer model number",
        ),

        sa.Column(
            "gtin",
            sa.String(length=50),
            nullable=True,
            comment="Global Trade Item Number such as GTIN, EAN, or UPC",
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'discovered'"),
            comment="Product lifecycle status",
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Indicates whether the product is active",
        ),

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),

        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["brand_id"],
            ["brands.id"],
            name="fk_products_brand_id",
        ),

        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="fk_products_category_id",
        ),

        sa.PrimaryKeyConstraint(
            "id",
            name="pk_products",
        ),

        sa.UniqueConstraint(
            "slug",
            name="uq_products_slug",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("products")