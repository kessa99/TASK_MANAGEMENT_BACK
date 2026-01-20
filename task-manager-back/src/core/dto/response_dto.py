"""
Format de réponse standardisé pour l'API
"""

from typing import TypeVar, Generic, Any
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Format de réponse standardisé

    Exemple succès:
    {
        "success": true,
        "data": { ... },
        "message": "Utilisateur créé avec succès",
        "errors": null
    }

    Exemple erreur:
    {
        "success": false,
        "data": null,
        "message": "Erreur de validation",
        "errors": [{"field": "email", "message": "Email invalide"}]
    }
    """
    success: bool
    data: T | None = None
    message: str | None = None
    errors: list[dict[str, Any]] | None = None

    model_config = {"from_attributes": True}


class ApiError(BaseModel):
    """Détail d'une erreur"""
    field: str | None = None
    message: str
    code: str | None = None


class PaginatedData(BaseModel, Generic[T]):
    """Données paginées"""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée standardisée"""
    success: bool = True
    data: PaginatedData[T] | None = None
    message: str | None = None
    errors: list[dict[str, Any]] | None = None


# Helpers pour créer des réponses facilement
def success_response(
    data: Any = None,
    message: str | None = None
) -> dict:
    """Créer une réponse de succès"""
    return {
        "success": True,
        "data": data,
        "message": message,
        "errors": None,
    }


def error_response(
    message: str,
    errors: list[dict] | None = None
) -> dict:
    """Créer une réponse d'erreur"""
    return {
        "success": False,
        "data": None,
        "message": message,
        "errors": errors,
    }


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str | None = None
) -> dict:
    """Créer une réponse paginée"""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
        "message": message,
        "errors": None,
    }
