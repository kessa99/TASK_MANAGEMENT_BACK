"""
Use Case: Récupérer les tâches d'un utilisateur
"""

from uuid import UUID
from dataclasses import dataclass
from core.useCase.base import UseCase
from core.dto.task_dto import TaskResponseDTO
from core.entities.user import User, UserRole
from core.repositories.task_repository import TaskRepository
from core.errors.base import AuthorizationError
from interface.http.mappers.task_mapper import map_task_entity_to_response


@dataclass
class GetUserTasksInput:
    """Input pour récupérer les tâches d'un utilisateur"""
    user_id: UUID
    current_user: User


class GetUserTasksUseCase(UseCase[GetUserTasksInput, list[TaskResponseDTO]]):
    """
    Use Case pour récupérer les tâches assignées à un utilisateur

    Règles métier:
    - OWNER peut voir les tâches de n'importe quel utilisateur
    - MEMBER peut voir uniquement ses propres tâches
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, input_dto: GetUserTasksInput) -> list[TaskResponseDTO]:
        """
        Récupérer les tâches d'un utilisateur

        Args:
            input_dto: ID de l'utilisateur et utilisateur courant

        Returns:
            Liste des tâches assignées

        Raises:
            AuthorizationError: Si un MEMBER tente de voir les tâches d'un autre
        """
        # MEMBER ne peut voir que ses propres tâches
        if input_dto.current_user.role == UserRole.MEMBER:
            if input_dto.current_user.id != input_dto.user_id:
                raise AuthorizationError(
                    message="Vous ne pouvez voir que vos propres tâches",
                    code="ACCESS_DENIED"
                )

        tasks = self.task_repository.get_tasks_for_user(input_dto.user_id)
        return [map_task_entity_to_response(task) for task in tasks]
