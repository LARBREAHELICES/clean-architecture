"""add password to User

Revision ID: 512dfcb2d75d
Revises: fb3b9f037667
Create Date: 2025-05-11 18:08:46.647834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512dfcb2d75d'
down_revision: Union[str, None] = 'fb3b9f037667'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Ajout de la colonne password non nullable avec valeur par défaut vide
    op.add_column(
        'user',
        sa.Column(
            'password',
            sa.String(),
            nullable=False,
            server_default=sa.text("''")  # chaîne vide par défaut
        )
    )

def downgrade():
    op.drop_column('user', 'password')