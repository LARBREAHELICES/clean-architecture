"""create user table with example data

Revision ID: 282736008fc4
Revises: 
Create Date: 2025-04-23 09:26:22.657306
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision: str = '282736008fc4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Création de la table utilisateur
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('bonus', sa.Integer),
    )

    # Données d'exemple (optionnel)
    user_table = table(
        'user',
        column('id', Integer),
        column('username', String),
        column('age', Integer),
        column('bonus', Integer)
    )

    op.bulk_insert(user_table, [
        {"id": 1, "username": "admin", "bonus": 100, "age" : 25},
        {"id": 2, "username": "guest", "bonus": 10, "age" : 18},
    ])


def downgrade() -> None:
    op.drop_table('user')
