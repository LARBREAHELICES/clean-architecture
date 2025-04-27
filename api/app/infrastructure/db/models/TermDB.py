# app/domain/models/term.py
from sqlmodel import SQLModel, Field,Relationship
from typing import List, Optional
from app.infrastructure.db.models.User_Term_DB import User_Term_DB


class TermDB(SQLModel, table=True):
    __tablename__ = 'term'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relation many-to-many avec les User
    users: List["UserDB"] = Relationship(back_populates="terms", link_model=User_Term_DB)