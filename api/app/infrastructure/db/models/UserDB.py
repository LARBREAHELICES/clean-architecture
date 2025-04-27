# app/domain/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

class UserBase(SQLModel):
    username: str
    bonus: int

class UserCreate(UserBase):
    pass  # utilisé pour la création

class UserDB(UserBase, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    terms: List["TermDB"] = Relationship(back_populates="users", link_model=User_Term_DB)
    
