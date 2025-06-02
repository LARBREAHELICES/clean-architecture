"""add role_id to user table

Revision ID: 117bc80b5e52
Revises: 599d12692b0e
Create Date: 2025-06-01 07:28:22.755235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '117bc80b5e52'
down_revision: Union[str, None] = '599d12692b0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("role_id", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_user_role_id",  # nom de la contrainte
        "user",             # table source
        "role",             # table cible
        ["role_id"],        # colonne source
        ["id"]              # colonne cible
    )


def downgrade() -> None:
    op.drop_constraint("fk_user_role_id", "user", type_="foreignkey")
    op.drop_column("user", "role_id")
