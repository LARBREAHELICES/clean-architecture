from pydantic import BaseModel

# Schéma pour la création d'un terme
class TermCreateRequest(BaseModel):
    name: str

# Schéma pour la réponse d'un terme (avec id généré)
class TermResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # Pour que Pydantic puisse lire les objets SQLAlchemy/SQLModel comme des dicts