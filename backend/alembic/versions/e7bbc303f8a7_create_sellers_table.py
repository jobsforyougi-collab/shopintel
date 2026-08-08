"""create sellers table

Revision ID: e7bbc303f8a7
Revises: 85a4d24d0dda
Create Date: 2026-08-08 14:37:43.641858

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7bbc303f8a7"
down_revision: Union[str, Sequence[str], None] = "85a4d24d0dda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "sellers",

        sa.Column(
            "name",
            sa.String(length=200),
            nullable=False,
            comment="Canonical seller name",
        ),

        sa.Column(
            "normalized_name",
            sa.String(length=200),
            nullable=False,
            comment="Normalized seller name used for identity matching",
        ),

        sa.Column(
            "website",
            sa.String(length=500),
            nullable=True,
            comment="Seller's official website",
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Optional canonical seller description",
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Indicates whether the seller is active",
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

        sa.PrimaryKeyConstraint(
            "id",
            name="pk_sellers",
        ),
    )

    op.create_index(
        "ix_sellers_normalized_name",
        "sellers",
        ["normalized_name"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_sellers_normalized_name",
        table_name="sellers",
    )

    op.drop_table("sellers")