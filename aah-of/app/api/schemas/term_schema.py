from pydantic import BaseModel

# Base commune
class TermBase(BaseModel):
    name: str

# Pour la création (n’a pas besoin d’`id`)
class TermCreateRequest(TermBase):
    pass

# Pour la réponse (hérite de `TermBase` + id)
class TermResponse(TermBase):
    id: int

    class Config:
        orm_mode = True
