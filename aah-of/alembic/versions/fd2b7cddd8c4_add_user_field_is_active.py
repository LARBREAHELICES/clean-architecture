"""add user field is_active

Revision ID: fd2b7cddd8c4
Revises: edeb740202cf
Create Date: 2025-05-15 04:44:43.712903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd2b7cddd8c4'
down_revision: Union[str, None] = 'edeb740202cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False,  server_default=sa.text('True')))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'is_active')

