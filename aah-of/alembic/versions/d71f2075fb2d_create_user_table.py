"""create user table

Revision ID: d71f2075fb2d
Revises: 
Create Date: 2025-04-27 07:20:53.389580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd71f2075fb2d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('bonus', sa.Integer, nullable=True)
    )
    
     # --- Insérer des données
    op.bulk_insert(
        sa.table(
            'user',
            sa.column('username', sa.String),
            sa.column('bonus', sa.Integer),
        ),
        [
            {'username': 'alice', 'bonus': 100},
            {'username': 'bob', 'bonus': 200},
            {'username': 'charlie', 'bonus': 0},
            {'username': 'alan', 'bonus': 10},
            {'username': 'steph', 'bonus': 20},
            {'username': 'john', 'bonus': 0},
        ]
    )
    
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
    pass
