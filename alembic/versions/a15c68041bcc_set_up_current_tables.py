"""set up current tables

Revision ID: a15c68041bcc
Revises: 
Create Date: 2022-09-28 21:38:30.759580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a15c68041bcc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('inventory', sa.Integer(), nullable=False),
    sa.Column('on_sale_price', sa.Float(), server_default='0.0', nullable=False),
    sa.Column('on_sale', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('payment_method', sa.String(), nullable=False),
    sa.Column('credit', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products_sold',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sale_id'], ['sales.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id', 'sale_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_sold')
    op.drop_table('sales')
    op.drop_table('products')
    op.drop_table('users')
    # ### end Alembic commands ###
