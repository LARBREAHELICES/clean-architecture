from app.domain.models.Term import Term
from app.infrastructure.db.models import TermDB

class TermMapper:
    
    @staticmethod
    def to_domain(term_db: TermDB) -> Term:
        """
        Convertir un modèle de base de données TermDB en un modèle métier Term
        """
        return Term(id=term_db.id, name=term_db.name)
    
    @staticmethod
    def to_db(term: Term) -> TermDB:
        """
        Convertir un modèle métier Term en un modèle de base de données TermDB
        """
        return TermDB(id=term.id, name=term.name)
