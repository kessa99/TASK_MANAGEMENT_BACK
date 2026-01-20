"""
Exceptions liées aux utilisateurs
"""

from core.errors.base import NotFoundError, AuthenticationError, AuthorizationError, ConflictError


class UserNotFoundError(NotFoundError):
    """Utilisateur non trouvé"""

    def __init__(self, message: str = "Utilisateur non trouvé"):
        super().__init__(
            message=message,
            code="USER_NOT_FOUND",
        )


class UserAlreadyExistsError(ConflictError):
    """Un utilisateur avec cet email existe déjà"""

    def __init__(self, message: str = "Un utilisateur avec cet email existe déjà"):
        super().__init__(
            message=message,
            code="USER_ALREADY_EXISTS",
            field="email",
        )


class UserNotVerifiedError(AuthorizationError):
    """Compte utilisateur non vérifié"""

    def __init__(self, message: str = "Compte non vérifié"):
        super().__init__(
            message=message,
            code="USER_NOT_VERIFIED",
        )


class InvalidCredentialsError(AuthenticationError):
    """Identifiants invalides"""

    def __init__(self, message: str = "Email ou mot de passe incorrect"):
        super().__init__(
            message=message,
            code="INVALID_CREDENTIALS",
        )
