"""
fichier principale
"""

from fastapi import FastAPI
from .infrastructure.database.init_db import init_db

def create_app() -> FastAPI:
    """Création de l'application FastAPI"""
    app = FastAPI(
        title="Task Manager API",
        version="1.0.0",
    )
    return app

app = create_app()

@app.on_event("startup")
async def startup():
    """
    Fonction d'événement de démarrage de l'application
    """
    init_db()

# @app.on_event("shutdown")
# async def shutdown():
#     """
#     Fonction d'événement de fermeture de l'application
#     """
#     await engine.dispose()