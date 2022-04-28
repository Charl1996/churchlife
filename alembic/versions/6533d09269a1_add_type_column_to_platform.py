"""Add type column to Platform

Revision ID: 6533d09269a1
Revises: 4f3b723beab3
Create Date: 2022-04-24 22:06:08.062838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6533d09269a1'
down_revision = '4f3b723beab3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('platform', sa.Column('type', sa.String))


def downgrade():
    op.drop_column('platform', 'type')
