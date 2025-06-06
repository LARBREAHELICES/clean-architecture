import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

class Settings:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.secret_key = SECRET_KEY
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.algorithm = ALGORITHM
        self.env = ENV
        self.debug = DEBUG

settings = Settings()