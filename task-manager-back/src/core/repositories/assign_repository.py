"""
Core repository interface pour les assignations
"""

from abc import ABC, abstractmethod
from uuid import UUID
from core.entities.assign import Assign


class AssignRepository(ABC):
    """
    Interface du repository pour les assignations
    """

    @abstractmethod
    def save(self, assign: Assign) -> Assign:
        """Sauvegarder une assignation"""
        pass

    @abstractmethod
    def find_all(self) -> list[Assign]:
        """Trouver toutes les assignations"""
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> Assign | None:
        """Trouver une assignation par son id"""
        pass

    @abstractmethod
    def update(self, assign: Assign) -> Assign:
        """Mettre à jour une assignation"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Supprimer une assignation"""
        pass

    @abstractmethod
    def get_assignments_for_user(self, user_id: UUID) -> list[Assign]:
        """Trouver les assignations d'un utilisateur"""
        pass
