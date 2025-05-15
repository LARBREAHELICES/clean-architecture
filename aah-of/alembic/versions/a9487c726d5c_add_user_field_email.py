"""add user field email

Revision ID: a9487c726d5c
Revises: 1c0a9f99bfca
Create Date: 2025-05-14 08:26:10.203271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9487c726d5c'
down_revision: Union[str, None] = '1c0a9f99bfca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=True))
    connection = op.get_bind()
    
    updates = [
        ("d07639ae-0f27-4e44-b25c-feca295e5e58", "alice@example.com"),
        ("ce7a70e2-93f5-4dc6-ba11-36cfcb5d4886", "bob@example.com"),
        ("16fe0198-473d-4ade-a205-31271acfee25", "charlie@example.com"),
        ("bb4ed92a-4f10-483c-9b5f-429764b40fba", "alan@example.com"),
        ("988f4b12-a665-4434-a831-13782e842324", "steph@example.com"),
        ("4ccb008e-794e-46cc-bf3a-16fe22c7fb25", "john@example.com"),
    ]
    for user_id, email in updates:
        connection.execute(
            sa.text("""
                UPDATE "user"
                SET email = :email
                WHERE id = :user_id;
            """),
            {"email": email, "user_id": user_id}
        )


def downgrade():
    op.drop_column('user', 'email')
