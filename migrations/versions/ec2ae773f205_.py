"""empty message

Revision ID: ec2ae773f205
Revises: f0f93c736dfe
Create Date: 2024-06-17 10:43:02.053181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2ae773f205'
down_revision = 'f0f93c736dfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lists_books',
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['list_id'], ['lists.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lists_books')
    # ### end Alembic commands ###
