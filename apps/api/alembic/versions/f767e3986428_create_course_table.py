"""create course table

Revision ID: f767e3986428
Revises: 814b47cc500e
Create Date: 2025-06-02 06:09:46.844426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f767e3986428'
down_revision: Union[str, None] = '814b47cc500e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Table course
    op.create_table(
        'course',
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()'), nullable=False),
        sa.Column('is_published', sa.Boolean, default=False, nullable=False)
    )

    # Table d'association course_user
    op.create_table(
        'course_user',
        sa.Column('course_id', sa.String(36), sa.ForeignKey('course.id', ondelete="CASCADE"), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    )

def downgrade():
    op.drop_table('course_user')
    op.drop_table('course')