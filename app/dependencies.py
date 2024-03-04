from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuration de la connexion à la base de données
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root@db/carbon_emissions"

# Création de l'engine SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Création d'une session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()

# Dépendance à utiliser avec les routes FastAPI pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
