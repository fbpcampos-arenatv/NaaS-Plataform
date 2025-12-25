"""criar itens

Revision ID: 0001
Revises: 
Create Date: 2024-12-25 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "itens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=120), nullable=False, unique=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("itens")
