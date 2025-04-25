# app/domain/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
<<<<<<< HEAD:api/app/domain/models.py
    age: int
    bonus: int = Field(default=0)
=======
    bonus: int
>>>>>>> upstream/main:api/app/domain/models/User.py
