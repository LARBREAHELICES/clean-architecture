# app/interfaces/schemas/user_schema.py
from pydantic import BaseModel

from app.api.schemas.term_schema import TermResponse
from typing import List

class UserCreateRequest(BaseModel):
    username: str
    bonus: int

class UserResponse(BaseModel):
    id: int
    username: str
    bonus: int

    class Config:
        orm_mode = True  # pour supporter SQLAlchemy/SQLModel

class UserTermResponse(BaseModel):
    id: int
    username: str
    bonus: int
    terms : List[TermResponse]

    class Config:
        orm_mode = True