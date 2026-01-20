"""
Exceptions de base
"""

from fastapi import status


class AppError(Exception):
    """
    Exception de base pour toutes les erreurs métier

    Attributes:
        message: Message d'erreur
        code: Code d'erreur (ex: "USER_NOT_FOUND")
        status_code: Code HTTP associé
        field: Champ concerné (optionnel)
    """

    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        field: str | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.field = field
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convertir l'erreur en dictionnaire"""
        return {
            "message": self.message,
            "code": self.code,
            "field": self.field,
        }


class NotFoundError(AppError):
    """Ressource non trouvée"""

    def __init__(
        self,
        message: str = "Ressource non trouvée",
        code: str = "NOT_FOUND",
        field: str | None = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_404_NOT_FOUND,
            field=field,
        )


class ValidationError(AppError):
    """Erreur de validation"""

    def __init__(
        self,
        message: str = "Erreur de validation",
        code: str = "VALIDATION_ERROR",
        field: str | None = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            field=field,
        )


class AuthenticationError(AppError):
    """Erreur d'authentification"""

    def __init__(
        self,
        message: str = "Non authentifié",
        code: str = "AUTHENTICATION_ERROR",
        field: str | None = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_401_UNAUTHORIZED,
            field=field,
        )


class AuthorizationError(AppError):
    """Erreur d'autorisation"""

    def __init__(
        self,
        message: str = "Accès non autorisé",
        code: str = "AUTHORIZATION_ERROR",
        field: str | None = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_403_FORBIDDEN,
            field=field,
        )


class ConflictError(AppError):
    """Conflit (ressource déjà existante, etc.)"""

    def __init__(
        self,
        message: str = "Conflit",
        code: str = "CONFLICT",
        field: str | None = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_409_CONFLICT,
            field=field,
        )
