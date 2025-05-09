# app/domain/models/user_term.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User_Term_DB(SQLModel, table=True):
    __tablename__ = 'user_term'
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    term_id: Optional[int] = Field(default=None, foreign_key="term.id", primary_key=True)
