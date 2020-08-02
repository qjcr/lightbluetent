"""Initial migration

Revision ID: 9c2aef525df6
Revises: 
Create Date: 2020-08-02 15:00:55.759439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c2aef525df6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('societies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('short_name', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('welcome_text', sa.String(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('banner_text', sa.String(), nullable=True),
    sa.Column('banner_color', sa.String(), nullable=True),
    sa.Column('mute_on_start', sa.Boolean(), nullable=False),
    sa.Column('disable_private_chat', sa.Boolean(), nullable=False),
    sa.Column('attendee_pw', sa.String(), nullable=False),
    sa.Column('moderator_pw', sa.String(), nullable=False),
    sa.Column('uid', sa.String(), nullable=False),
    sa.Column('bbb_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('attendee_pw'),
    sa.UniqueConstraint('bbb_id'),
    sa.UniqueConstraint('moderator_pw'),
    sa.UniqueConstraint('short_name'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('crsid', sa.String(length=7), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('society_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['society_id'], ['societies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('societies')
    # ### end Alembic commands ###
