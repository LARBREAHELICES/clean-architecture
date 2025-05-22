# app/infrastructure/db/database.py
from sqlmodel import Session, create_engine, SQLModel

from app.config.dev import settings

# ⚡ On importe les modèles d'infrastructure !
from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.TermDB import TermDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

from app.infrastructure.db.models.ReportingSummaryDB import ReportingSummaryDB

# Créer un moteur
engine = create_engine(settings.database_url)

# Session locale
def SessionLocal() -> Session:
    return Session(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer les tables
def create_db()->None:
    SQLModel.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")