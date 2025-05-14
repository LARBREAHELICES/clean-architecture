# app/domain/models/user.py
import uuid

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

class UserBase(SQLModel):
    username: str
    bonus: int
    email: Optional[str] = None
    is_active: bool = False

class UserCreate(UserBase):
    pass  # utilisé pour la création

class UserAuth(UserBase):
    password: str 

class UserDB(UserBase, table=True):
    __tablename__ = "user"

    id: Optional[str] =Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    
    terms: List["TermDB"] = Relationship(back_populates="users", link_model=User_Term_DB)
    
