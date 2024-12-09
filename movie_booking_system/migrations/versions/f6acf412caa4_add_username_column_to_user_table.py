"""Add username column to user table

Revision ID: f6acf412caa4
Revises: 80a6338433e4
Create Date: 2024-11-26 03:50:15.809338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6acf412caa4'
down_revision = '80a6338433e4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=80), nullable=False))
        batch_op.create_unique_constraint('uq_user_username', ['username'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.drop_column('username')


    # ### end Alembic commands ###
