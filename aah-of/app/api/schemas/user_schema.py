from pydantic import BaseModel
from typing import List
from app.api.schemas.term_schema import TermResponse

# Base user info commune à tous les schémas de réponse
class UserBase(BaseModel):
    id: int
    username: str
    bonus: int

    class Config:
        orm_mode = True

# Schéma pour la création
class UserCreateRequest(BaseModel):
    username: str
    bonus: int

# Schéma de base pour la réponse simple
class UserResponse(UserBase):
    pass

# Schéma de réponse avec les termes associés
class UserTermResponse(UserBase):
    terms: List[TermResponse]
