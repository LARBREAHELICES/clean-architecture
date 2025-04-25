import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
from sqlmodel import SQLModel  # Importer SQLModel

# Charger les variables d'environnement depuis .env
load_dotenv()

# Importer ton modèle principal ou tous les modèles utilisés
from app.domain.models.user import User  

# Config Alembic
config = context.config
fileConfig(config.config_file_name)

# Charger l’URL de la base de données depuis .env
DATABASE_URL = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Associer les métadonnées de SQLModel
target_metadata = SQLModel.metadata
