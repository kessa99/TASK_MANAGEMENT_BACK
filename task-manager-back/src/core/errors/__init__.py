"""
Exceptions métier
"""

from core.errors.base import (
    AppError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
)
from core.errors.user_errors import (
    UserNotFoundError,
    UserAlreadyExistsError,
    UserNotVerifiedError,
    InvalidCredentialsError,
)
from core.errors.task_errors import (
    TaskNotFoundError,
    TaskAccessDeniedError,
)
from core.errors.invitation_errors import (
    InvitationNotFoundError,
    InvitationExpiredError,
    InvitationAlreadyAcceptedError,
    InvitationAlreadyExistsError,
)

__all__ = [
    # Base
    "AppError",
    "NotFoundError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "ConflictError",
    # User
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "UserNotVerifiedError",
    "InvalidCredentialsError",
    # Task
    "TaskNotFoundError",
    "TaskAccessDeniedError",
    # Invitation
    "InvitationNotFoundError",
    "InvitationExpiredError",
    "InvitationAlreadyAcceptedError",
    "InvitationAlreadyExistsError",
]
