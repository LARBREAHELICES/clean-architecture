from fastapi import APIRouter, Depends, HTTPException
from app.domain.models.User import User
from app.domain.models.Term import Term
from app.domain.models.UserResponse import UserResponse
from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl

# sérialisation API schema FastAPI
from app.infrastructure.db.schemas.user_schema import UserCreateRequest

from sqlmodel import Session
from typing import List

router = APIRouter()

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer un utilisateur
@router.post("/user/create", response_model=User)
async def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)  # connexion à l'infrastructure
    user_service = UserService(user_repository)  # le service a besoin de la dépendance user_repository
    
    return user_service.create_user(user)

# Obtenir un utilisateur par ID
@router.get("/user/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_service = UserService(user_repository)
    
    return user_service.get_user_by_id(user_id)

# Lister tous les utilisateurs
@router.get("/users", response_model=List[User])
def list_users(db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_service = UserService(user_repository)
    
    return user_service.list_users()

# Ajouter un term à un utilisateur existant
@router.post("/user/{user_id}/add_term/{term_id}", response_model=User)
def add_term_to_user(user_id: int, term_id: int, db: Session = Depends(get_db)):
    term_repository = TermRepositoryImpl(db)
    term_service = TermService(term_repository)
    
    # Ajouter le terme à l'utilisateur
    term_service.add_term_to_user(user_id, term_id)
    
    # Récupérer l'utilisateur avec ses termes mis à jour
    user_service = UserService(UserRepositoryImpl(db))
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Lister les terms d'un utilisateur donné
@router.get("/user/{user_id}/terms", response_model=UserResponse)
def list_user_terms(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_service = UserService(user_repository)
    
    return user_service.list_terms_for_user(user_id)

# Lister tous les terms
@router.get("/terms", response_model=List[Term])
def list_terms(db: Session = Depends(get_db)):
    term_repository = TermRepositoryImpl(db)
    term_service = TermService(term_repository)
    
    return term_service.list_terms()

# Lister un term donné
@router.get("/term/{term_id}", response_model=Term)
def list_terms(term_id: int, db: Session = Depends(get_db)):
    term_repository = TermRepositoryImpl(db)
    term_service = TermService(term_repository)
    
    return term_service.get_term_by_id(term_id)

# Lister un term donné
@router.post("/term/create", response_model=Term)
def list_terms(term: Term, db: Session = Depends(get_db)):
    term_repository = TermRepositoryImpl(db)
    term_service = TermService(term_repository)
    
    return term_service.create(term)