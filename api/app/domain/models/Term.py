# app/domain/models/term.py
from sqlmodel import SQLModel, Field,Relationship
from typing import List, Optional
from app.domain.models.User_Term import UserTerm

class Term(SQLModel, table=True):
    __tablename__ = 'term'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relation many-to-many avec les User
    users: List["User"] = Relationship(back_populates="terms", link_model=UserTerm)