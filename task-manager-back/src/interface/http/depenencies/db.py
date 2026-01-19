"""
Dépendances HTTP
"""

from config.database import SessionLocal

def get_db():
    """
    Dépendance HTTP de la base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()