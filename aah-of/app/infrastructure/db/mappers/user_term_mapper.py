from app.infrastructure.db.models import User_Term_DB
from app.domain.models.User import User
from app.domain.models.Term import Term

class UserTermMapper:
    
    @staticmethod
    def to_db(user_id: int, term_id: int) -> User_Term_DB:
        """
        Convertir une relation utilisateur-terme en entrée dans la table d'association User_Term_DB
        """
        return User_Term_DB(user_id=user_id, term_id=term_id)
    
    @staticmethod
    def to_domain(user_term_db: User_Term_DB) -> tuple[User, Term]:
        """
        Convertir une entrée de la table d'association User_Term_DB en objets domaine User et Term
        """
        return User(id=user_term_db.user_id), Term(id=user_term_db.term_id)
