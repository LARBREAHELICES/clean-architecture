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
        ("d07639ae-0f27-4e44-b25c-feca295e5e58",hashed_password ),
        ("ce7a70e2-93f5-4dc6-ba11-36cfcb5d4886", hashed_password),
        ("16fe0198-473d-4ade-a205-31271acfee25", hashed_password),
        ("bb4ed92a-4f10-483c-9b5f-429764b40fba", hashed_password),
        ("988f4b12-a665-4434-a831-13782e842324", hashed_password),
        ("4ccb008e-794e-46cc-bf3a-16fe22c7fb25", hashed_password),
    ]
    
    connection = op.get_bind()
    for user_id, password in updates:
        connection.execute(
            sa.text("""
                UPDATE "user"
                SET  password = :password
                WHERE id = :user_id;
            """),
            { "password": password, "user_id": user_id}
        )
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'password')
