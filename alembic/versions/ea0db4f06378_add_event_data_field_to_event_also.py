"""Add event_data field to event also

Revision ID: ea0db4f06378
Revises: e9245e418b8d
Create Date: 2022-05-21 09:50:33.802684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea0db4f06378'
down_revision = 'e9245e418b8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('event_data', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'event_data')
    # ### end Alembic commands ###