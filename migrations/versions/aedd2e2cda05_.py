"""empty message

Revision ID: aedd2e2cda05
Revises: 7f5bd4095737
Create Date: 2020-03-22 11:04:24.872913

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aedd2e2cda05'
down_revision = '7f5bd4095737'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurants', 'blurhash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('blurhash', mysql.VARCHAR(length=200), nullable=True))
    # ### end Alembic commands ###
