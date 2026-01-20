"""
Core repository interface pour les tâches
"""

from abc import ABC, abstractmethod
from uuid import UUID
from core.entities.task import Task


class TaskRepository(ABC):
    """
    Interface du repository pour les tâches
    """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """Sauvegarder une tâche"""
        pass

    @abstractmethod
    def find_all(self) -> list[Task]:
        """Trouver toutes les tâches"""
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> Task | None:
        """Trouver une tâche par son id"""
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        """Mettre à jour une tâche"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Supprimer une tâche"""
        pass

    @abstractmethod
    def get_tasks_for_user(self, user_id: UUID) -> list[Task]:
        """Trouver les tâches assignées à un utilisateur"""
        pass
