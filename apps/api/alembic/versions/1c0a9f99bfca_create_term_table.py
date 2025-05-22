"""Initial migration with UUID primary keys and associations

Revision ID: init_uuid_schema
Revises: 
Create Date: 2025-05-13

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '1c0a9f99bfca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # UUIDs pour users
    alice_id = str(uuid.uuid4())
    bob_id = str(uuid.uuid4())
    charlie_id = str(uuid.uuid4())
    alan_id = str(uuid.uuid4())
    steph_id = str(uuid.uuid4())
    john_id = str(uuid.uuid4())

    # UUIDs pour terms
    tech_id = str(uuid.uuid4())
    science_id = str(uuid.uuid4())
    music_id = str(uuid.uuid4())
    art_id = str(uuid.uuid4())
    sports_id = str(uuid.uuid4())

    # Créer la table user
    op.create_table(
        'user',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('bonus', sa.Integer, nullable=True),
    )

    op.bulk_insert(
        sa.table(
            'user',
            sa.column('id', sa.String),
            sa.column('username', sa.String),
            sa.column('bonus', sa.Integer),
        ),
        [
            {'id': alice_id, 'username': 'alice', 'bonus': 100},
            {'id': bob_id, 'username': 'bob', 'bonus': 200},
            {'id': charlie_id, 'username': 'charlie', 'bonus': 0},
            {'id': alan_id, 'username': 'alan', 'bonus': 10},
            {'id': steph_id, 'username': 'steph', 'bonus': 20},
            {'id': john_id, 'username': 'john', 'bonus': 0},
        ]
    )

    # Créer la table term
    op.create_table(
        'term',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
    )

    op.bulk_insert(
        sa.table(
            'term',
            sa.column('id', sa.String),
            sa.column('name', sa.String),
        ),
        [
            {'id': tech_id, 'name': 'Technology'},
            {'id': science_id, 'name': 'Science'},
            {'id': music_id, 'name': 'Music'},
            {'id': art_id, 'name': 'Art'},
            {'id': sports_id, 'name': 'Sports'},
        ]
    )

    # Créer la table d'association user_term
    op.create_table(
        'user_term',
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('term_id', sa.String(length=36), sa.ForeignKey('term.id'), primary_key=True),
    )

    op.bulk_insert(
        sa.table(
            'user_term',
            sa.column('user_id', sa.String),
            sa.column('term_id', sa.String),
        ),
        [
            {'user_id': alice_id, 'term_id': tech_id},
            {'user_id': alice_id, 'term_id': science_id},
            {'user_id': bob_id, 'term_id': music_id},
            {'user_id': bob_id, 'term_id': art_id},
            {'user_id': charlie_id, 'term_id': sports_id},
        ]
    )

def downgrade() -> None:
    op.drop_table('user_term')
    op.drop_table('term')
    op.drop_table('user')
