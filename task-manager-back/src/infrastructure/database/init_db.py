"""
Initialisation de la base de données
"""

from src.config.database import engine
from src.infrastructure.database.models.base import Base

def init_db():
    """
    Initialisation de la base de données
    """
    Base.metadata.create_all(engine)