# app/infrastructure/db/database.py
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os

# ⚡ On importe les modèles d'infrastructure !
from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.TermDB import TermDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base
DATABASE_URL = os.getenv("DATABASE_URL")

# Créer un moteur
engine = create_engine(DATABASE_URL)

# Session locale
def SessionLocal() -> Session:
    return Session(bind=engine)

# Créer les tables
def create_db():
    SQLModel.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")