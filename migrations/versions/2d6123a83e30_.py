"""empty message

Revision ID: 2d6123a83e30
Revises: c27851d0a551
Create Date: 2020-03-18 23:29:42.221684

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2d6123a83e30'
down_revision = 'c27851d0a551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurants', 'image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('image', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
