"""initial migrations

Revision ID: d69743d7371a
Revises: 
Create Date: 2021-12-28 12:59:06.583117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd69743d7371a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('register', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('f_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('register', schema=None) as batch_op:
        batch_op.add_column(sa.Column('f_name', sa.VARCHAR(length=100), nullable=True))
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
