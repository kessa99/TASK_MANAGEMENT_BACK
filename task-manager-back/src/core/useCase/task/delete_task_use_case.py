"""
Use Case: Supprimer une tâche
"""

from uuid import UUID
from core.useCase.base import UseCase
from core.repositories.task_repository import TaskRepository
from core.errors.task_errors import TaskNotFoundError


class DeleteTaskUseCase(UseCase[UUID, bool]):
    """
    Use Case pour supprimer une tâche

    Règles métier:
    - Seul OWNER peut supprimer (vérifié au niveau route)
    - La tâche doit exister
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: UUID) -> bool:
        """
        Supprimer une tâche

        Args:
            task_id: ID de la tâche à supprimer

        Returns:
            True si supprimé

        Raises:
            TaskNotFoundError: Si la tâche n'existe pas
        """
        task = self.task_repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()

        self.task_repository.delete(task_id)
        return True
