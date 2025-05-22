"""add is_certifying in reporting_summary

Revision ID: a412376bcde9
Revises: 9a10426786e5
Create Date: 2025-05-21 14:53:16.730780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a412376bcde9'
down_revision: Union[str, None] = '9a10426786e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('reporting_summary', sa.Column('is_certifying', sa.Boolean(), nullable=False, server_default='true'))

def downgrade():
    op.drop_column('reporting_summary', 'is_certifying')
