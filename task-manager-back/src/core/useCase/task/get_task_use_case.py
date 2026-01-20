"""
Use Case: Récupérer une tâche
"""

from uuid import UUID
from dataclasses import dataclass
from core.useCase.base import UseCase
from core.dto.task_dto import TaskResponseDTO
from core.entities.user import User, UserRole
from core.repositories.task_repository import TaskRepository
from core.errors.task_errors import TaskNotFoundError, TaskAccessDeniedError
from interface.http.mappers.task_mapper import map_task_entity_to_response


@dataclass
class GetTaskInput:
    """Input pour récupérer une tâche"""
    task_id: UUID
    current_user: User


class GetTaskUseCase(UseCase[GetTaskInput, TaskResponseDTO]):
    """
    Use Case pour récupérer une tâche par son ID

    Règles métier:
    - OWNER peut voir toutes les tâches
    - MEMBER peut voir uniquement les tâches qui lui sont assignées
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, input_dto: GetTaskInput) -> TaskResponseDTO:
        """
        Récupérer une tâche

        Args:
            input_dto: ID de la tâche et utilisateur courant

        Returns:
            TaskResponseDTO: La tâche

        Raises:
            TaskNotFoundError: Si la tâche n'existe pas
            TaskAccessDeniedError: Si l'utilisateur n'a pas accès
        """
        task = self.task_repository.find_by_id(input_dto.task_id)
        if task is None:
            raise TaskNotFoundError()

        # Vérifier l'accès pour les MEMBER
        if input_dto.current_user.role == UserRole.MEMBER:
            if input_dto.current_user.id not in task.assigned_to:
                raise TaskAccessDeniedError()

        return map_task_entity_to_response(task)
