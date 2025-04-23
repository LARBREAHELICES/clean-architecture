import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# 👇 Ajouter le chemin de ton projet pour l'import des modèles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer ta base de données et tes modèles ici
from app.domain.models import User  # Si ton modèle User est dans app/domain/models.py
from app.infrastructure.db import engine  # Si ton engine est configuré dans app/infrastructure/db.py

# Configurer le fichier de log d'Alémic
config = context.config
fileConfig(config.config_file_name)

# Fournir la MetaData pour les comparaisons (c'est ce qu'Alémic attend)
target_metadata = SQLModel.metadata  # C'est la métadonnée que Alembic va utiliser

# Fonction principale pour la migration
def run_migrations_online():
    # Connecter à la base de données avec la configuration d'Alembic
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # Utile pour vérifier les changements de type entre les versions
        )

        with context.begin_transaction():
            context.run_migrations()
