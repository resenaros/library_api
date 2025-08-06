"""Rename item_name to name in items table

Revision ID: 40e8bb4d91b0
Revises: 
Create Date: 2025-07-31 19:30:50.968260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '40e8bb4d91b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('items', 'item_name',
        new_column_name='name',
        existing_type=sa.String(255),
        nullable=False
    )

def downgrade():
    op.alter_column('items', 'name',
        new_column_name='item_name',
        existing_type=sa.String(255),
        nullable=False
    )