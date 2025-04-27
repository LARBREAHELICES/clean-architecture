from pydantic import BaseModel
from typing import List

class TermResponse(BaseModel):
    name: str
    id: int

class UserResponse(BaseModel):
    username: str
    bonus: int
    terms: List[TermResponse]  # Liste des termes associés à l'utilisateur

    class Config:
        orm_mode = True  # Permet à Pydantic de lire les objets SQLAlchemy/SQLModel comme des dicts
