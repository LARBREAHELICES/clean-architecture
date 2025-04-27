# app/domain/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.domain.models.User_Term import UserTerm

class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    bonus: int

    # Relation many-to-many avec les Term
    terms: List["Term"] = Relationship(back_populates="users", link_model=UserTerm)