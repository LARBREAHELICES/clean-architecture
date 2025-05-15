# app/api/term_routes.py
from fastapi import APIRouter, Depends, HTTPException

from app.domain.dtos.term_dto import TermDTO, TermCreateDTO

from app.application.controllers.term_controller import TermController
from app.api.deps import get_term_controller

from typing import List

router = APIRouter()

# Lister tous les termes
@router.get("/all", response_model=List[TermDTO])
def list_terms(term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.get_all_terms()

# Créer un terme
@router.post("/", response_model=TermDTO)
def create_term(term: TermCreateDTO, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.create_term(term)

# Lister un terme donné
@router.get("/{term_id}", response_model=TermDTO)
def get_term_by_id(term_id: str, term_controller: TermController = Depends(get_term_controller)):
    
    return term_controller.get_term_by_id(term_id)
