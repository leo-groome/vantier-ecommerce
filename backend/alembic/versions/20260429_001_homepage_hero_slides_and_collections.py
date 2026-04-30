"""Homepage CMS: hero_slides and collections tables.

Revision ID: 20260429_001
Revises: 96c7cd855248
Create Date: 2026-04-29
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260429_001"
down_revision = "20260426_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------ hero_slides
    op.create_table(
        "hero_slides",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("subtitle", sa.String(300), nullable=True),
        sa.Column("cta_text", sa.String(100), nullable=False, server_default="Explore the Collection"),
        sa.Column("cta_url", sa.String(500), nullable=False, server_default="/shop"),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("theme", sa.String(10), nullable=False, server_default="dark"),
        sa.Column("position", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------ collections
    op.create_table(
        "collections",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("tagline", sa.String(300), nullable=True),
        sa.Column("label", sa.String(100), nullable=True),
        sa.Column("price_from", sa.String(50), nullable=True),
        sa.Column("link_url", sa.String(500), nullable=False, server_default="/shop"),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("position", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("collections")
    op.drop_table("hero_slides")
