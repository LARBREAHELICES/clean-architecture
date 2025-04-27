from fastapi import APIRouter, Depends
from app.domain.models.User import User
from app.domain.models.TermResponse import UserResponse
from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.infrastructure.db.database import SessionLocal

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.user_fake_repository_impl import UserFakeRepositoryImpl
from sqlmodel import Session

from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl

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
def create_user(user: User, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db) # connexion à l'infrastructure
    user_service = UserService(user_repository) # le servie à besoin de la dépendance user_repository
    
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
@router.post("/user/{user_id}/add_term/{term_id}")
def add_term_to_user(user_id: int, term_id: int, db: Session = Depends(get_db)):
    term_repository = TermRepositoryImpl(db)
    term_service = TermService(term_repository)
    term_service.add_term_to_user(user_id, term_id)
    
    term_name = term_service.get_term_by_id(term_id)
    
    return {"message": f"Term ajouté {term_name.name} avec succès à l'utilisateur"}

# Lister les terms d'un utilisateur donné
@router.get("/user/{user_id}/terms", response_model=UserResponse)
def list_users(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_service = UserService(user_repository)
    
    return user_service.list_terms_for_user(user_id)

# Lister tous les utilisateurs
@router.get("/fake/users", response_model=List[User])
def list_fake_users():
    user_repository = UserFakeRepositoryImpl()
    # le fait de changer de UserFakeRepositoryImpl ne change pas le service
    user_service = UserService(user_repository)
    
    return  user_service.list_users()
