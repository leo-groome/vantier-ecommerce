"""Add percent discount upper bound and partial unique index for default address.

Revision ID: 20260409_002
Revises: 20260409_001
Create Date: 2026-04-09
"""

from alembic import op

revision = "20260409_002"
down_revision = "20260409_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Prevent percent discounts from exceeding 100%
    op.create_check_constraint(
        "ck_discount_percent_max_100",
        "discount_codes",
        "NOT (type = 'percent' AND value > 100)",
    )

    # Ensure each user can only have one default address
    op.execute(
        """
        CREATE UNIQUE INDEX uq_saved_address_default_per_user
        ON saved_addresses (neon_auth_user_id)
        WHERE is_default = true
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_saved_address_default_per_user")
    op.drop_constraint("ck_discount_percent_max_100", "discount_codes", type_="check")
