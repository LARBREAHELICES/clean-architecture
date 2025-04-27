# app/infrastructure/db/database.py
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os

from app.domain.models.User import User 

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Créer un moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session locale
def SessionLocal() -> Session:
    return Session(autocommit=False, autoflush=False, bind=engine)


def create_db():
    # Créer toutes les tables dans la base de données
    SQLModel.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")
    