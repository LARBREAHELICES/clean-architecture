"""add default roles and permissions

Revision ID: 814b47cc500e
Revises: 117bc80b5e52
Create Date: 2025-06-02 05:58:38.915318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '814b47cc500e'
down_revision: Union[str, None] = '117bc80b5e52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()

    # === Création des rôles ===
    roles = {
        'admin': str(uuid.uuid4()),
        'teacher': str(uuid.uuid4()),
        'leader': str(uuid.uuid4()),
        'visitor': str(uuid.uuid4())
    }

    for name, role_id in roles.items():
        connection.execute(
            sa.text("INSERT INTO role (id, name) VALUES (:id, :name)"),
            {"id": role_id, "name": name}
        )

    # === Création des permissions ===
    permissions = {
        'view_course': str(uuid.uuid4()),
        'edit_course': str(uuid.uuid4()),
        'delete_course': str(uuid.uuid4()),
        'assign_roles': str(uuid.uuid4())
    }

    for name, perm_id in permissions.items():
        connection.execute(
            sa.text("INSERT INTO permission (id, name) VALUES (:id, :name)"),
            {"id": perm_id, "name": name}
        )

    # === Association rôles/permissions ===
    role_permissions = {
        'admin': ['view_course', 'edit_course', 'delete_course', 'assign_roles'],
        'teacher': ['view_course', 'edit_course'],
        'leader': ['view_course'],
        'visitor': ['view_course'],
    }

    for role, perms in role_permissions.items():
        role_id = roles[role]
        for perm in perms:
            perm_id = permissions[perm]
            connection.execute(
                sa.text("INSERT INTO role_permission (role_id, permission_id) VALUES (:role_id, :perm_id)"),
                {"role_id": role_id, "perm_id": perm_id}
            )

    # === Mise à jour des utilisateurs ===
    # (adapte selon ta logique ; ici on met tous les users existants en 'visitor')
    visitor_role_id = roles['visitor']
    connection.execute(
        sa.text("UPDATE \"user\" SET role_id = :role_id WHERE role_id IS NULL"),
        {"role_id": visitor_role_id}
    )


def downgrade():
    connection = op.get_bind()

    # Supprime les relations
    connection.execute(sa.text("DELETE FROM role_permission"))

    # Supprime permissions
    connection.execute(sa.text("DELETE FROM permission"))

    # Supprime rôles
    connection.execute(sa.text("DELETE FROM role"))

    # Reset user roles
    connection.execute(sa.text("UPDATE \"user\" SET role_id = NULL"))