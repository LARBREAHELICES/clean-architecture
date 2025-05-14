"""Add new fields to user table

Revision ID: 7efdc35fd4ab
Revises: 1c0a9f99bfca
Create Date: 2025-05-14 05:48:53.564521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers, used by Alembic.
revision: str = '7efdc35fd4ab'
down_revision: Union[str, None] = '1c0a9f99bfca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1. Ajout des colonnes "email", "password" et "is_active"
    op.add_column('user', sa.Column('email', sa.String(255), nullable=True))
    op.add_column('user', sa.Column('password', sa.String(255), nullable=True))
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=True, default=True))

    # 2. Hash du mot de passe (admin123)
    hashed_password = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')

    # 3. Mise à jour des valeurs de email, password et is_active pour chaque utilisateur
    connection = op.get_bind()
    updates = [
        ("c5ddb585-8f05-4583-89cd-af3c0b73497c", "alice@example.com", hashed_password),
        ("fed6ef57-bbf9-4c86-b0d4-1dadb19e94be", "bob@example.com", hashed_password),
        ("e4a0c0b9-f85f-4bd1-8670-c6c9403cb85e", "charlie@example.com", hashed_password),
        ("0d67711a-f40c-4694-aca1-83ec4cd97676", "alan@example.com", hashed_password),
        ("de8a6e20-4dee-4365-961e-09129ce61ad7", "steph@example.com", hashed_password),
        ("8d5cc9b5-0ac4-4504-ae97-9345466dcbb8", "john@example.com", hashed_password),
        ("0003b935-a8e7-4f39-9bd3-376d30edcead", "yvette@example.com", hashed_password),
    ]

    for user_id, email, password in updates:
        connection.execute(
            sa.text("""
                UPDATE "user"
                SET email = :email, password = :password, is_active = :is_active
                WHERE id = :user_id;
            """),
            {"email": email, "password": password, "is_active": True, "user_id": user_id}
        )

def downgrade():
    op.drop_column('user', 'email')
    op.drop_column('user', 'password')
    op.drop_column('user', 'is_active')
