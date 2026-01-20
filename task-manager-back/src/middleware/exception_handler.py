"""
Gestionnaire global des exceptions
Transforme toutes les exceptions en format de réponse standardisé
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from core.dto.response_dto import error_response
from core.errors.base import AppError


async def app_exception_handler(
    request: Request,
    exc: AppError
) -> JSONResponse:
    """
    Gère les exceptions métier personnalisées (AppError)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
            errors=[exc.to_dict()]
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    """
    Gère les HTTPException de FastAPI
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.detail,
            errors=[{"message": exc.detail, "code": "HTTP_ERROR"}]
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Gère les erreurs de validation Pydantic/FastAPI
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "code": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Erreur de validation",
            errors=errors
        ),
    )


async def pydantic_exception_handler(
    request: Request,
    exc: ValidationError
) -> JSONResponse:
    """
    Gère les erreurs de validation Pydantic directes
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "code": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Erreur de validation",
            errors=errors
        ),
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Gère toutes les autres exceptions non gérées
    """
    # En production, ne pas exposer les détails de l'erreur
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="Erreur interne du serveur",
            errors=[{"message": str(exc), "code": "INTERNAL_ERROR"}]
        ),
    )
