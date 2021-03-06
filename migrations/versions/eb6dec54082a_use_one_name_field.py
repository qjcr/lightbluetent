"""Use one name field

Revision ID: eb6dec54082a
Revises: f1278c9a2e87
Create Date: 2020-09-26 17:02:38.315413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb6dec54082a"
down_revision = "f1278c9a2e87"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("full_name", sa.String(), nullable=True))
    # join existing database fields
    op.execute(
        """
        update users as target set full_name = (
        select  first_name||' '||surname
        from users as source where source.id = target.id
        );
        """
    )
    op.alter_column("users", "full_name", nullable=False)
    # set both fields as nullable so we don't get errors between migrations
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("users", "surname", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "full_name")
    op.alter_column("users", "surname", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
