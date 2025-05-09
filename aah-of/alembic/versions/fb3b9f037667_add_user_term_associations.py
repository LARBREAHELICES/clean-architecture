"""add user_term associations

Revision ID: fb3b9f037667
Revises: 1c0a9f99bfca
Create Date: 2025-05-09 14:19:16.811031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb3b9f037667'
down_revision: Union[str, None] = '1c0a9f99bfca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    """Associe les users aux termes via la table user_term."""
    user_term_table = sa.table(
        'user_term',
        sa.column('user_id', sa.Integer),
        sa.column('term_id', sa.Integer),
    )

    # Insertion des associations (basée sur les IDs insérés dans les migrations précédentes)
    op.bulk_insert(
        user_term_table,
        [
            {'user_id': 1, 'term_id': 1},  # alice → Technology
            {'user_id': 1, 'term_id': 2},  # alice → Science
            {'user_id': 2, 'term_id': 3},  # bob → Music
            {'user_id': 2, 'term_id': 4},  # bob → Art
            {'user_id': 3, 'term_id': 5},  # charlie → Sports
        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM user_term")
