"""Add status column to OrganisationsUser

Revision ID: 781a75f4897a
Revises: 2e4475076af0
Create Date: 2022-04-23 16:17:08.017774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '781a75f4897a'
down_revision = '2e4475076af0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('organisations_users', sa.Column('status', sa.String))


def downgrade():
    op.drop_column('organisations_users', 'status')
