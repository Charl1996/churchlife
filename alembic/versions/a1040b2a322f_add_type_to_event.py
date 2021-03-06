"""Add type to event

Revision ID: a1040b2a322f
Revises: 56fffb8948a7
Create Date: 2022-05-03 20:35:17.983471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1040b2a322f'
down_revision = '56fffb8948a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('type', sa.String(), nullable=False))
    op.drop_column('tracking_events', 'interval')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tracking_events', sa.Column('interval', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('events', 'type')
    # ### end Alembic commands ###
