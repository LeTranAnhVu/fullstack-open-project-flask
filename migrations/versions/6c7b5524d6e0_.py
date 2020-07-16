"""empty message

Revision ID: 6c7b5524d6e0
Revises: 72ff26fd3bf9
Create Date: 2020-03-27 18:05:17.038151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c7b5524d6e0'
down_revision = '72ff26fd3bf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('order_places', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'order_places')
    # ### end Alembic commands ###