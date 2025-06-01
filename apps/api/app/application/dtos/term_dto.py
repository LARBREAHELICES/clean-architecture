from typing import Optional, List
from pydantic import BaseModel

from uuid import UUID

# Base commune pour création, lecture, update interne
class TermBaseDTO(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }

# DTO pour la création (POST)
class TermCreateDTO(TermBaseDTO):
    pass

# DTO pour la mise à jour (PATCH / PUT)
class TermUpdateDTO(BaseModel):
    name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# DTO pour la lecture simple (GET /terms, etc.)
class TermDTO(TermBaseDTO):
    id: UUID

# DTO avec utilisateurs associés (GET /terms/{id}/users)
class TermUsersDTO(TermDTO):
    
    users: List["UserDTO"] = []  # Utilisation de l'annotation différée
