"""add google_id in user model

Revision ID: e9c5b5c525b2
Revises: 925ea930a0ce
Create Date: 2023-12-03 13:17:26.471873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e9c5b5c525b2'
down_revision = '925ea930a0ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('google_id', sa.String(length=255), nullable=True))
        batch_op.alter_column('password_hashed',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.create_unique_constraint(None, ['google_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password_hashed',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.drop_column('google_id')

    # ### end Alembic commands ###
