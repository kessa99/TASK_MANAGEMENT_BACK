"""
Exceptions liées aux tâches
"""

from core.errors.base import NotFoundError, AuthorizationError


class TaskNotFoundError(NotFoundError):
    """Tâche non trouvée"""

    def __init__(self, message: str = "Tâche non trouvée"):
        super().__init__(
            message=message,
            code="TASK_NOT_FOUND",
        )


class TaskAccessDeniedError(AuthorizationError):
    """Accès à la tâche refusé"""

    def __init__(self, message: str = "Vous n'avez pas accès à cette tâche"):
        super().__init__(
            message=message,
            code="TASK_ACCESS_DENIED",
        )
