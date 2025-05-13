from typing import List, Optional
from pydantic import BaseModel

from app.domain.dtos.term_dto import TermDTO

# Base commune utilisée en interne (app + infra)
class UserBaseDTO(BaseModel):
    username: str
    bonus: float

    class Config:
        orm_mode = True
        from_attributes = True

# Pour la création (POST) — sans id
class UserCreateDTO(UserBaseDTO):
    pass

# Pour la mise à jour (PUT / PATCH)
class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    bonus: Optional[float] = None

    class Config:
        orm_mode = True
        from_attributes = True

# Pour la lecture (GET)
class UserDTO(UserBaseDTO):
    id: str

# Pour les cas avec relations
class UserWithTermsDTO(UserDTO):
    terms: List[TermDTO] = []  # Utilisation de l'annotation différée
