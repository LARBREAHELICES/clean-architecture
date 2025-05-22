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
        ( "alice", "alice@example.com"),
        ( "bob", "bob@example.com"),
        ( "charlie", "charlie@example.com"),
        ( "alan", "alan@example.com"),
        ( "steph", "steph@example.com"),
        ( "john", "john@example.com"),
    ]
    for username, email in updates:
        connection.execute(
            sa.text("""
                UPDATE "user"
                SET email = :email
                WHERE username = :username;
            """),
            {"email": email, "username": username}
        )


def downgrade():
    op.drop_column('user', 'email')
