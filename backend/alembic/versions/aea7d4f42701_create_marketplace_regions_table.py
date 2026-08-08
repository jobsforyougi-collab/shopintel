"""create marketplace regions table

Revision ID: aea7d4f42701
Revises: 1245d36b7ccd
Create Date: 2026-08-08 13:55:20.688998

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aea7d4f42701"
down_revision: Union[str, Sequence[str], None] = "1245d36b7ccd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "marketplace_regions",

        sa.Column(
            "marketplace_id",
            sa.UUID(),
            nullable=False,
            comment="Marketplace that owns this region",
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
            comment="Human-readable marketplace region name",
        ),

        sa.Column(
            "code",
            sa.String(length=20),
            nullable=False,
            comment="Unique region code within the marketplace",
        ),

        sa.Column(
            "country_code",
            sa.String(length=2),
            nullable=False,
            comment="ISO 3166-1 alpha-2 country code",
        ),

        sa.Column(
            "currency_code",
            sa.String(length=3),
            nullable=False,
            comment="ISO 4217 currency code",
        ),

        sa.Column(
            "locale",
            sa.String(length=20),
            nullable=False,
            comment="Default locale for the marketplace region",
        ),

        sa.Column(
            "timezone",
            sa.String(length=50),
            nullable=False,
            comment="IANA timezone identifier",
        ),

        sa.Column(
            "base_url",
            sa.String(length=255),
            nullable=False,
            comment="Regional marketplace base URL",
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Indicates whether the marketplace region is active",
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
            ["marketplace_id"],
            ["marketplaces.id"],
            name="fk_marketplace_regions_marketplace_id",
        ),

        sa.PrimaryKeyConstraint(
            "id",
            name="pk_marketplace_regions",
        ),

        sa.UniqueConstraint(
            "marketplace_id",
            "code",
            name="uq_marketplace_regions_marketplace_code",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("marketplace_regions")