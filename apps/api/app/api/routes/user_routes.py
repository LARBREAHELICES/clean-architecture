# app/api/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.application.controllers.user_controller import UserController

from app.application.dtos.user_dto import UserDTO, UserWithTermsDTO, UserCreateDTO

from app.api.deps import get_user_controller
from typing import List

router = APIRouter()

# Créer un utilisateur
@router.post("/", response_model=UserDTO)
async def create_user(user: UserCreateDTO, user_controller: UserController = Depends(get_user_controller)):
    return user_controller.create_user(user)

# Lister tous les utilisateurs
@router.get("/all", response_model=List[UserDTO])
def list_users(user_controller: UserController = Depends(get_user_controller)):
    
    return user_controller.list_users()

# Obtenir un utilisateur par ID
@router.get("/{user_id}", response_model=UserDTO)
def get_user(user_id: str, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/terms", response_model=UserWithTermsDTO)
def get_user_with_terms(user_id: str, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.get_user_with_terms(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/{user_id}/assign-terms", response_model=UserWithTermsDTO)
async def assign_terms(
    user_id: str,
    term_ids: List[str],
    controller: UserController = Depends(get_user_controller)
):
    return controller.assign_terms_to_user(user_id, term_ids)

@router.get("/term/{term_id}/users", response_model=List[UserDTO])
def get_users_for_term(
    term_id: str,
    controller: UserController = Depends(get_user_controller)
):
    return controller.get_users_by_term(term_id)