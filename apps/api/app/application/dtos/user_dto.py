from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

from app.application.dtos.term_dto import TermDTO


# Base commune utilisée en interne (app + infra)
class UserBaseDTO(BaseModel):
    username: str
    bonus: float
    email: Optional[str]
    is_active: bool

    model_config = {
        "from_attributes": True
    }


# Pour la création (POST) — sans id
class UserCreateDTO(UserBaseDTO):
    password: str


# Pour la mise à jour (PUT / PATCH)
class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    bonus: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


# Pour la lecture (GET)
class UserDTO(UserBaseDTO):
    id: UUID


# Pour les cas avec relations
class UserWithTermsDTO(UserDTO):
    terms: List[TermDTO] = Field(default_factory=list)
