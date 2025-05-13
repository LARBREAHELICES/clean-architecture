# app/api/term_routes.py
from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.term_schema import TermCreateRequest, TermResponse
from app.application.controllers.term_controller import TermController
from app.api.deps import get_term_controller

from typing import List

router = APIRouter()

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
