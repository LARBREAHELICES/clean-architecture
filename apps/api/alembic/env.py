import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
from sqlmodel import SQLModel

# ⚡ Charger les variables d'environnement
load_dotenv()

# ⚡ Importer TOUS tes modèles d'infrastructure
from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.TermDB import TermDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

# ⚙️ Config Alembic
config = context.config
fileConfig(config.config_file_name)

# Charger DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL n'est pas défini dans .env")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Associer les métadonnées de SQLModel
target_metadata = SQLModel.metadata

def run_migrations_online() -> None:
    """Exécuter les migrations en mode online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# Lancer les migrations
run_migrations_online()
