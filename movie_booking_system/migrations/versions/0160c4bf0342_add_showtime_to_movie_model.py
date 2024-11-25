"""Add showtime to Movie model

Revision ID: 0160c4bf0342
Revises: 3559e5c7a240
Create Date: 2024-11-24 20:11:21.932790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0160c4bf0342'
down_revision = '3559e5c7a240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('showtime', sa.String(length=50), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('admin_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.INTEGER(), nullable=True))

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('showtime')

    # ### end Alembic commands ###