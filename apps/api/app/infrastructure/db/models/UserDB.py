import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.infrastructure.db.models.User_Term_DB import User_Term_DB

from app.infrastructure.db.models.RoleDB import RoleDB

# Base commune (pas de table ici)
class UserBase(SQLModel): # type: ignore[misc]
    username: str
    bonus: int
    email: str
    is_active: bool

# DTO pour création (ex : depuis API ou fixture)
class UserCreateDB(UserBase):
    password: str

# Modèle base de données
class UserDB(UserBase, table=True):  # type: ignore[misc]
    __tablename__ = "user"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True) # type: ignore[misc]
    password: str
    role_id: Optional[str] = Field(default=None, foreign_key="role.id")
    role: Optional[RoleDB] = Relationship(back_populates="users")
    terms: List["TermDB"] = Relationship(back_populates="users", link_model=User_Term_DB) # type: ignore[misc]



