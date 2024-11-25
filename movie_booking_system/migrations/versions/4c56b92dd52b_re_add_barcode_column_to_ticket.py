"""Re-add barcode column to Ticket

Revision ID: 4c56b92dd52b
Revises: 7ebee99132dd
Create Date: 2024-11-24 23:59:58.485348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c56b92dd52b'
down_revision = '7ebee99132dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_ticket_barcode', ['barcode'])


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_constraint('uq_ticket_barcode', type_='unique')
        batch_op.drop_column('barcode')


    # ### end Alembic commands ###