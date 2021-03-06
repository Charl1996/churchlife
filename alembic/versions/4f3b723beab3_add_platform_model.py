"""add platform model

Revision ID: 4f3b723beab3
Revises: 781a75f4897a
Create Date: 2022-04-24 19:39:37.719981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3b723beab3'
down_revision = '781a75f4897a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('subdomain', sa.String(), nullable=True),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_platform_id'), 'platform', ['id'], unique=False)
    op.create_index(op.f('ix_platform_organisation_id'), 'platform', ['organisation_id'], unique=False)
    op.create_index(op.f('ix_platform_slug'), 'platform', ['slug'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_platform_slug'), table_name='platform')
    op.drop_index(op.f('ix_platform_organisation_id'), table_name='platform')
    op.drop_index(op.f('ix_platform_id'), table_name='platform')
    op.drop_table('platform')
    # ### end Alembic commands ###
