# app/domain/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

class UserDB(SQLModel, table=True):
    __tablename__ = 'user'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    bonus: int

    # Relation many-to-many avec les Term
    terms: List["Term"] = Relationship(back_populates="users", link_model=User_Term_DB)