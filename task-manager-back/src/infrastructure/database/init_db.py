"""
Initialisation de la base de données
"""

from config.database import engine
from infrastructure.database.models import Base

def init_db():
    """
    Initialisation de la base de données
    """
    Base.metadata.create_all(bind=engine)