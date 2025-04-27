# app/api/term_routes.py
from fastapi import APIRouter, Depends

from app.application.controllers.term_controller import TermController
from app.domain.models.Term import Term
from typing import List

from app.infrastructure.db.database import get_db
from sqlmodel import Session

from app.infrastructure.db.schemas.term_schema import TermCreateRequest

router = APIRouter()

# Dépendance pour obtenir le contrôleur
def get_term_controller(db: Session = Depends(get_db)) -> TermController:
    return TermController(db)

# Lister tous les termes
@router.get("/all", response_model=List[Term])
def list_terms(term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.list_terms()

# Créer un terme
@router.post("/create", response_model=Term)
def create_term(term: TermCreateRequest, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.create_term(term)

# Lister un terme donné
@router.get("/{term_id}", response_model=Term)
def get_term_by_id(term_id: int, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.list_term(term_id)
