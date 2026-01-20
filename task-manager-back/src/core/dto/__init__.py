"""
Data Transfer Objects (DTOs)
"""

from core.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)
from core.dto.task_dto import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TaskResponseDTO,
)
from core.dto.assign_dto import (
    AssignCreateDTO,
    AssignResponseDTO,
)
from core.dto.auth_dto import (
    LoginDTO,
    RegisterDTO,
    TokenDTO,
    TokenPayloadDTO,
    RefreshTokenDTO,
)
from core.dto.invitation_dto import (
    InviteCreateDTO,
    InviteAcceptDTO,
    InvitationResponseDTO,
    InvitationDetailDTO,
)
from core.dto.response_dto import (
    ApiResponse,
    ApiError,
    PaginatedData,
    PaginatedResponse,
    success_response,
    error_response,
    paginated_response,
)

__all__ = [
    # User
    "UserCreateDTO",
    "UserUpdateDTO",
    "UserResponseDTO",
    # Task
    "TaskCreateDTO",
    "TaskUpdateDTO",
    "TaskResponseDTO",
    # Assign
    "AssignCreateDTO",
    "AssignResponseDTO",
    # Auth
    "LoginDTO",
    "RegisterDTO",
    "TokenDTO",
    "TokenPayloadDTO",
    "RefreshTokenDTO",
    # Invitation
    "InviteCreateDTO",
    "InviteAcceptDTO",
    "InvitationResponseDTO",
    "InvitationDetailDTO",
    # Response
    "ApiResponse",
    "ApiError",
    "PaginatedData",
    "PaginatedResponse",
    "success_response",
    "error_response",
    "paginated_response",
]
