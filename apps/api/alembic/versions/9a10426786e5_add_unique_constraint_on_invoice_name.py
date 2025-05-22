"""add unique constraint on invoice_name

Revision ID: 9a10426786e5
Revises: 1509304d5a16
Create Date: 2025-05-21 13:23:57.528120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a10426786e5'
down_revision: Union[str, None] = '1509304d5a16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        constraint_name='uq_invoice_name',
        table_name='reporting_summary',
        columns=['invoice_name']
    )

def downgrade():
    op.drop_constraint(
        constraint_name='uq_invoice_name',
        table_name='reporting_summary',
        type_='unique'
    )

