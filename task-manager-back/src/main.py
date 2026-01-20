"""
Fichier principal - Point d'entrée de l'application
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
# /home/attito/Boulot/compo/TASK_MANAGEMENT_BACK/task-manager-back/src/infrastructure/database/init_db.py
from infrastructure.database.init_db import init_db
from interface.http.routes.user_routes import router as user_router
from interface.http.routes.task_routes import router as task_router
from interface.http.routes.assign_routes import router as assign_router
from interface.http.routes.auth_routes import router as auth_router
from interface.http.routes.invitation_routes import router as invitation_router
from middleware.exception_handler import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    pydantic_exception_handler,
    generic_exception_handler,
)
from core.errors.base import AppError
from core.dto.response_dto import success_response


def create_app() -> FastAPI:
    """Création de l'application FastAPI"""
    app = FastAPI(
        title="Task Manager API",
        description="API de gestion de tâches",
        version="1.0.0",
    )

    # Gestionnaires d'exceptions globaux (ordre important: du plus spécifique au plus général)
    app.add_exception_handler(AppError, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Enregistrement des routes
    app.include_router(auth_router, prefix="/api")
    app.include_router(user_router, prefix="/api")
    app.include_router(task_router, prefix="/api")
    app.include_router(assign_router, prefix="/api")
    app.include_router(invitation_router, prefix="/api")

    return app


app = create_app()


@app.on_event("startup")
async def startup():
    """Initialisation de la base de données au démarrage"""
    init_db()


@app.get("/health", tags=["Health"])
def health_check():
    """Vérification de l'état de l'API"""
    return success_response(
        data={"status": "ok"},
        message="API opérationnelle"
    )
