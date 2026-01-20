"""
Use Case: Récupérer toutes les tâches
"""

from core.useCase.base import UseCase
from core.dto.task_dto import TaskResponseDTO
from core.entities.user import User, UserRole
from core.repositories.task_repository import TaskRepository
from interface.http.mappers.task_mapper import map_task_entity_to_response


class GetAllTasksUseCase(UseCase[User, list[TaskResponseDTO]]):
    """
    Use Case pour récupérer toutes les tâches

    Règles métier:
    - OWNER voit toutes les tâches
    - MEMBER voit uniquement ses tâches assignées
    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, current_user: User) -> list[TaskResponseDTO]:
        """
        Récupérer les tâches selon le rôle

        Args:
            current_user: L'utilisateur courant

        Returns:
            Liste des tâches accessibles
        """
        if current_user.role == UserRole.OWNER:
            tasks = self.task_repository.find_all()
        else:
            tasks = self.task_repository.get_tasks_for_user(current_user.id)

        return [map_task_entity_to_response(task) for task in tasks]
