"""create categories table

Revision ID: 2b6a4af4b00c
Revises: 7c48376e8838
Create Date: 2026-08-06 18:02:14.095997

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b6a4af4b00c"
down_revision: Union[str, Sequence[str], None] = "7c48376e8838"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "categories",

        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
            comment="Category name",
        ),

        sa.Column(
            "slug",
            sa.String(length=150),
            nullable=False,
            comment="Unique URL-friendly category slug",
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Optional category description",
        ),

        sa.Column(
            "parent_id",
            sa.UUID(),
            nullable=True,
            comment="Parent category ID",
        ),

        sa.Column(
            "level",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
            comment="Depth level in category hierarchy",
        ),

        sa.Column(
            "is_leaf",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Indicates whether this category has children",
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Indicates whether the category is active",
        ),

        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["categories.id"],
            name="fk_categories_parent_id",
        ),

        sa.PrimaryKeyConstraint(
            "id",
            name="pk_categories",
        ),

        sa.UniqueConstraint(
            "slug",
            name="uq_categories_slug",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("categories")