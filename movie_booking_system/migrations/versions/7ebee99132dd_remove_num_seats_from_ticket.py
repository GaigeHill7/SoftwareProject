"""Remove num_seats from Ticket

Revision ID: 7ebee99132dd
Revises: 44cb9a0d17fb
Create Date: 2024-11-24 23:49:00.260470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ebee99132dd'
down_revision = '44cb9a0d17fb'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'num_seats' column exists before dropping it
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        existing_columns = sa.inspect(batch_op.get_bind()).get_columns('ticket')
        if any(col['name'] == 'num_seats' for col in existing_columns):
            batch_op.drop_column('num_seats')

    # ### end Alembic commands ###


def downgrade():
    # Re-add the 'num_seats' column to the 'ticket' table in case of downgrade
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num_seats', sa.Integer(), nullable=True))

    # ### end Alembic commands ###
