from app.domain.models.User import User
from app.infrastructure.db.models import UserDB, User_Term_DB
from app.infrastructure.db.models.TermDB import TermDB
from app.domain.models.Term import Term

class UserMapper:
    
    @staticmethod
    def to_domain(user_db: UserDB) -> User:
        """
        Convertir un modèle de base de données UserDB en un modèle métier User
        """
        terms = [Term(id=term.id, name=term.name) for term in user_db.terms]
        return User(id=user_db.id, username=user_db.username, bonus=user_db.bonus, terms=terms)
    
    @staticmethod
    def to_db(user: User) -> UserDB:
        """
        Convertir un modèle métier User en un modèle de base de données UserDB
        """
        user_db = UserDB(id=user.id, username=user.username, bonus=user.bonus)
        user_db.terms = [TermDB(id=term.id, name=term.name) for term in user.terms]
        return user_db
