"""
Use Case: Créer une tâche
"""

from uuid import uuid4
from datetime import datetime
from core.useCase.base import UseCase
from core.dto.task_dto import TaskCreateDTO, TaskResponseDTO
from core.entities.task import Task
from core.repositories.task_repository import TaskRepository
from interface.http.mappers.task_mapper import map_task_entity_to_response


class CreateTaskUseCase(UseCase[TaskCreateDTO, TaskResponseDTO]):
    """
    Use Case pour créer une nouvelle tâche

    Règles métier:
    - Le titre est obligatoire
    - Le statut par défaut est TODO
    - La priorité par défaut est MEDIUM
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, input_dto: TaskCreateDTO) -> TaskResponseDTO:
        """
        Créer une nouvelle tâche

        Args:
            input_dto: Données de création

        Returns:
            TaskResponseDTO: La tâche créée
        """
        now = datetime.utcnow()

        task = Task(
            id=uuid4(),
            title=input_dto.title,
            description=input_dto.description,
            status=input_dto.status,
            priority=input_dto.priority,
            start_date=input_dto.start_date,
            due_date=input_dto.due_date,
            assigned_to=input_dto.assigned_to,
            created_at=now,
            updated_at=now,
        )

        saved_task = self.task_repository.save(task)
        return map_task_entity_to_response(saved_task)
