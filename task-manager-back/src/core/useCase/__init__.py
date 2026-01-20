"""
Use Cases - Logique métier de l'application
"""

# Auth
from core.useCase.auth.register_use_case import RegisterUseCase
from core.useCase.auth.login_use_case import LoginUseCase
from core.useCase.auth.refresh_token_use_case import RefreshTokenUseCase

# User
from core.useCase.user.get_user_use_case import GetUserUseCase
from core.useCase.user.get_all_users_use_case import GetAllUsersUseCase

# Task
from core.useCase.task.create_task_use_case import CreateTaskUseCase
from core.useCase.task.get_task_use_case import GetTaskUseCase
from core.useCase.task.get_user_tasks_use_case import GetUserTasksUseCase

# Invitation
from core.useCase.invitation.create_invitation_use_case import CreateInvitationUseCase
from core.useCase.invitation.accept_invitation_use_case import AcceptInvitationUseCase

__all__ = [
    # Auth
    "RegisterUseCase",
    "LoginUseCase",
    "RefreshTokenUseCase",
    # User
    "GetUserUseCase",
    "GetAllUsersUseCase",
    # Task
    "CreateTaskUseCase",
    "GetTaskUseCase",
    "GetUserTasksUseCase",
    # Invitation
    "CreateInvitationUseCase",
    "AcceptInvitationUseCase",
]
