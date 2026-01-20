"""
Exceptions liées aux invitations
"""

from core.errors.base import NotFoundError, ValidationError, ConflictError


class InvitationNotFoundError(NotFoundError):
    """Invitation non trouvée"""

    def __init__(self, message: str = "Invitation non trouvée"):
        super().__init__(
            message=message,
            code="INVITATION_NOT_FOUND",
        )


class InvitationExpiredError(ValidationError):
    """Invitation expirée"""

    def __init__(self, message: str = "Cette invitation a expiré"):
        super().__init__(
            message=message,
            code="INVITATION_EXPIRED",
        )


class InvitationAlreadyAcceptedError(ValidationError):
    """Invitation déjà acceptée"""

    def __init__(self, message: str = "Cette invitation a déjà été acceptée"):
        super().__init__(
            message=message,
            code="INVITATION_ALREADY_ACCEPTED",
        )


class InvitationAlreadyExistsError(ConflictError):
    """Une invitation existe déjà pour cet email et cette tâche"""

    def __init__(self, message: str = "Une invitation est déjà en attente pour cet email et cette tâche"):
        super().__init__(
            message=message,
            code="INVITATION_ALREADY_EXISTS",
        )
