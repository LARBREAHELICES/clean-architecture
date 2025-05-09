# app/api/term_routes.py
from app.api.schemas.term_schema import TermCreateRequest, TermResponse
from app.application.controllers.term_controller import TermController
from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.db.database import get_db
from sqlmodel import Session
from typing import List

router = APIRouter()

# Dépendance pour obtenir le contrôleur
def get_term_controller(db: Session = Depends(get_db)) -> TermController:
    return TermController(db)

# Lister tous les termes
@router.get("/all", response_model=List[TermResponse])
def list_terms(term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.list_terms()

# Créer un terme
@router.post("/create", response_model=TermResponse)
def create_term(term: TermCreateRequest, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.create_term(term)

# Lister un terme donné
@router.get("/{term_id}", response_model=TermResponse)
def get_term_by_id(term_id: int, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.list_term(term_id)

@router.get("/{term_id}/users", response_model=None)
def get_term_with_users(term_id: int, user_controller: TermController = Depends(get_term_controller)):
    pass