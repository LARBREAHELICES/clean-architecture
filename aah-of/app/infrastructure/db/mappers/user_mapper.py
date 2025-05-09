from app.domain.models.User import User
from app.infrastructure.db.models.UserDB import UserDB

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