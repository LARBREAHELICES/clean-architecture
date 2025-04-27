from app.domain.models.User import User
from app.domain.models.UserResponse import UserResponse
from app.infrastructure.db.models import UserDB
from app.infrastructure.db.mappers.term_mapper import TermMapper
from app.domain.models.Term import Term

class UserReponseMapper:
    
    @staticmethod
    def to_domain(user_db: UserDB) -> UserResponse:
        """
        Convertir un modèle de base de données UserDB en un modèle métier User
        """
        
        return UserResponse(
            id=user_db.id, 
            username=user_db.username, 
            bonus=user_db.bonus, 
            terms=[ TermMapper.to_domain(termDB) for termDB in user_db.terms ]
        )
    