"""updated models

Revision ID: 2a989e753820
Revises: 
Create Date: 2023-06-25 12:02:51.444395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a989e753820'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('min_to_read', sa.Integer(), nullable=False),
    sa.Column('post_image', sa.String(length=120), nullable=False),
    sa.Column('created_on', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
