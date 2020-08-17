"""Add time_created to Society

Revision ID: 025a539edc8b
Revises: 9c2aef525df6
Create Date: 2020-08-17 23:32:16.095012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '025a539edc8b'
down_revision = '9c2aef525df6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('societies', sa.Column('time_created', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('time_created', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'time_created')
    op.drop_column('societies', 'time_created')
    # ### end Alembic commands ###
