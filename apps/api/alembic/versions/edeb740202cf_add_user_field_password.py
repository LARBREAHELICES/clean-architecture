"""add user field password

Revision ID: edeb740202cf
Revises: a9487c726d5c
Create Date: 2025-05-14 09:19:37.012143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import bcrypt 

# revision identifiers, used by Alembic.
revision: str = 'edeb740202cf'
down_revision: Union[str, None] = 'a9487c726d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    hashed_password = bcrypt.hashpw(b'admin', bcrypt.gensalt()).decode('utf-8')
    op.add_column('user', sa.Column('password', sa.String(255), nullable=True))
    
    updates = [
        ( "alice",hashed_password),
        ( "bob",hashed_password),
        ( "charlie", hashed_password),
        ( "alan", hashed_password),
        ( "steph",hashed_password),
        ( "john", hashed_password),
    ]
    
    connection = op.get_bind()
    for username, password in updates:
        connection.execute(
            sa.text("""
                UPDATE "user"
                SET  password = :password
                WHERE username = :username;
            """),
            { "password": password, "username": username}
        )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'password')
