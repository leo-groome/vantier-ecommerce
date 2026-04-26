"""Stub for revision applied directly to DB (migration file was lost).

Revision ID: 20260425_001
Revises: 96c7cd855248
Create Date: 2026-04-25

This revision was applied to the database but its file was lost.
It is a no-op stub to preserve the revision chain.
"""
from __future__ import annotations

from alembic import op  # noqa: F401

revision = "20260425_001"
down_revision = "96c7cd855248"
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
