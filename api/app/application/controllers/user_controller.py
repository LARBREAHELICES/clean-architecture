from fastapi import APIRouter, Depends
from app.domain.services.user_service import UserService
from app.domain.services.rating_service import RatingService

from app.domain.models.user import User
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.user_fake_repository_impl import UserFakeRepositoryImpl
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
@router.post("/users", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    user_repository = UserRepositoryImpl(db) # connexion à l'infrastructure
    user_service = UserService(user_repository) # le servie à besoin de la dépendance user_repository
    return user_service.create_user(user)

# Obtenir un utilisateur par ID
@router.get("/users/{user_id}", response_model=User)
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

# Lister tous les utilisateurs
@router.get("/fake/users", response_model=List[User])
def list_fake_users():
    user_repository = UserFakeRepositoryImpl()
    # le fait de changer de UserFakeRepositoryImpl ne change pas le service
    user_service = UserService(user_repository)
    
    return  user_service.list_users()



@router.get("/fake/users/{category}", response_model=List[User])
def list_fake_users(category: str):
    user_repository = UserFakeRepositoryImpl()
    # le fait de changer de UserFakeRepositoryImpl ne change pas le service
    user_service = RatingService(user_repository)
    
    return  user_service.sort_users_category_by_rating(category)