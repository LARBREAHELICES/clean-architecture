from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid

class RolePermissionDB(SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "role_permission"

    role_id: Optional[str] = Field(default_factory=uuid.uuid4, foreign_key="role.id", primary_key=True)  # type: ignore[misc]
    permission_id: Optional[str] = Field(default_factory=uuid.uuid4, foreign_key="permission.id", primary_key=True)  # type: ignore[misc]
class RoleDB(SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "role"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # type: ignore[misc]
    name: str  # ex : "admin", "trainer", "manager"

    permissions: List["PermissionDB"] = Relationship(back_populates="roles", link_model=RolePermissionDB)
    users: List["UserDB"] = Relationship(back_populates="role")# type: ignore[misc]
class PermissionDB(SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "permission"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # type: ignore[misc]
    name: str  # ex : "view_trainer_availability"

    roles: List[RoleDB] = Relationship(back_populates="permissions", link_model=RolePermissionDB)  # type: ignore[misc]



