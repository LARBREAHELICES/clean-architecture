"""Create term table

Revision ID: 1c0a9f99bfca
Revises: d71f2075fb2d
Create Date: 2025-04-27 08:09:55.400840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1c0a9f99bfca'
down_revision: Union[str, None] = 'd71f2075fb2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Créer la table "term"
    op.create_table(
        'term',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
    )

    # Créer la table d'association entre "user" et "term" pour une relation many-to-many
    op.create_table(
        'user_term',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('term_id', sa.Integer, sa.ForeignKey('term.id'), primary_key=True),
    )

    # Optionnel : insérer des données par défaut dans la table term (centres d'intérêt populaires)
    op.bulk_insert(
        sa.table(
            'term',
            sa.column('name', sa.String),
        ),
        [
            {'name': 'Technology'},
            {'name': 'Science'},
            {'name': 'Music'},
            {'name': 'Art'},
            {'name': 'Sports'},
        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    # Supprimer la table d'association
    op.drop_table('user_term')

    # Supprimer la table "term"
    op.drop_table('term')
