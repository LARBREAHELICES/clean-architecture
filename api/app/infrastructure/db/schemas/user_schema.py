# app/interfaces/schemas/user_schema.py
from pydantic import BaseModel
from typing import Optional

class UserCreateRequest(BaseModel):
    username: str
    bonus: int

class UserResponseDB(BaseModel):
    id: int
    username: str
    bonus: int

    class Config:
        orm_mode = True  # pour supporter SQLAlchemy/SQLModel
