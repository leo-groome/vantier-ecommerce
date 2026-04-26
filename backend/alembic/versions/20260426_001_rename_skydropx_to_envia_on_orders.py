"""Rename skydropx columns to envia on orders table.

Revision ID: 20260426_001
Revises: 20260425_001
Create Date: 2026-04-26

"""
from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260426_001"
down_revision = "20260425_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename shipping-provider columns: Skydropx → Envia
    op.alter_column("orders", "skydropx_shipment_id", new_column_name="envia_shipment_id")
    op.alter_column("orders", "label_url", new_column_name="envia_label_url")

    # Drop legacy Skydropx-specific columns no longer on the model
    op.drop_column("orders", "skydropx_rate_id")
    op.drop_column("orders", "skydropx_quotation_id")


def downgrade() -> None:
    # Re-add legacy columns
    import sqlalchemy as sa

    op.add_column("orders", sa.Column("skydropx_quotation_id", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("skydropx_rate_id", sa.String(), nullable=True))

    # Reverse renames
    op.alter_column("orders", "envia_label_url", new_column_name="label_url")
    op.alter_column("orders", "envia_shipment_id", new_column_name="skydropx_shipment_id")
