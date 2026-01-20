"""
Use Case: Mettre à jour une tâche
"""

from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from core.useCase.base import UseCase
from core.dto.task_dto import TaskUpdateDTO, TaskResponseDTO
from core.repositories.task_repository import TaskRepository
from core.errors.task_errors import TaskNotFoundError
from interface.http.mappers.task_mapper import map_task_entity_to_response


@dataclass
class UpdateTaskInput:
    """Input pour mettre à jour une tâche"""
    task_id: UUID
    dto: TaskUpdateDTO


class UpdateTaskUseCase(UseCase[UpdateTaskInput, TaskResponseDTO]):
    """
    Use Case pour mettre à jour une tâche

    Règles métier:
    - Seul OWNER peut modifier (vérifié au niveau route)
    - La tâche doit exister
    - Seuls les champs fournis sont mis à jour
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, input_dto: UpdateTaskInput) -> TaskResponseDTO:
        """
        Mettre à jour une tâche

        Args:
            input_dto: ID de la tâche et données à modifier

        Returns:
            TaskResponseDTO: La tâche mise à jour

        Raises:
            TaskNotFoundError: Si la tâche n'existe pas
        """
        task = self.task_repository.find_by_id(input_dto.task_id)
        if task is None:
            raise TaskNotFoundError()

        dto = input_dto.dto

        # Mettre à jour uniquement les champs fournis
        if dto.title is not None:
            task.title = dto.title
        if dto.description is not None:
            task.description = dto.description
        if dto.status is not None:
            task.status = dto.status
        if dto.priority is not None:
            task.priority = dto.priority
        if dto.start_date is not None:
            task.start_date = dto.start_date
        if dto.due_date is not None:
            task.due_date = dto.due_date
        if dto.assigned_to is not None:
            task.assigned_to = dto.assigned_to

        task.updated_at = datetime.utcnow()

        updated_task = self.task_repository.update(task)
        return map_task_entity_to_response(updated_task)
