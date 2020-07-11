"""empty message

Revision ID: 607c92214f49
Revises: 
Create Date: 2020-03-13 13:33:18.901290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '607c92214f49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=200), nullable=True),
    sa.Column('currency', sa.String(length=5), nullable=True),
    sa.Column('delivery_price', sa.Float(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('name', sa.String(length=300), nullable=True),
    sa.Column('online', sa.Boolean(), nullable=True),
    sa.Column('blurhash', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurants')
    # ### end Alembic commands ###