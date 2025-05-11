from app.domain.models.User import User, UserTerms, UserCreate
from app.infrastructure.db.models.UserDB import UserDB

from app.infrastructure.db.mappers.term_mapper import TermMapper

class UserMapper:
    
    @staticmethod
    def to_domain(user_db: UserDB) -> User:
        """
        Convertir un modèle de base de données UserDB en un modèle métier User
        """
        
        return User(
            id=user_db.id, 
            username=user_db.username, 
            bonus=user_db.bonus,
            email=user_db.email,
            disabled=user_db.disabled
            )
    
    @staticmethod
    def to_db(user: UserCreate) -> UserDB:
        """
        Convertir un modèle métier User en un modèle de base de données UserDB
        """
        return UserDB(
            username=user.username, 
            bonus=user.bonus,
            password = user.password,
            email=user.email
            )
    
    @staticmethod
    def to_domain_userterms(user_db: UserDB) -> UserTerms:
        return UserTerms(
            id=user_db.id,
            username=user_db.username,
            bonus=user_db.bonus,
            email=user_db.email,
            disabled=user_db.disabled,
            terms=[TermMapper.to_domain(term_db) for term_db in user_db.terms] if user_db.terms else []
        )