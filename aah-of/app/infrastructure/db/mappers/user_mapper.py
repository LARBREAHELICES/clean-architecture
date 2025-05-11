from app.domain.models.User import User, UserTerms
from app.infrastructure.db.models.UserDB import UserDB

from app.infrastructure.db.mappers.term_mapper import TermMapper

class UserMapper:
    
    @staticmethod
    def to_domain(user_db: UserDB) -> User:
        """
        Convertir un modèle de base de données UserDB en un modèle métier User
        """
        
        return User(id=user_db.id, username=user_db.username, bonus=user_db.bonus)
    
    @staticmethod
    def to_db(user: User) -> UserDB:
        """
        Convertir un modèle métier User en un modèle de base de données UserDB
        """
        return UserDB(username=user.username, bonus=user.bonus)
    
    @staticmethod
    def to_domain_userterms(user_db: UserDB) -> UserTerms:
        return UserTerms(
            id=user_db.id,
            username=user_db.username,
            bonus=user_db.bonus,
            terms=[TermMapper.to_domain(term_db) for term_db in user_db.terms] if user_db.terms else []
        )