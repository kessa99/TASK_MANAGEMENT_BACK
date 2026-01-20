"""
Core repository interface pour les utilisateurs
"""

from abc import ABC, abstractmethod
from uuid import UUID
from core.entities.user import User


class UserRepository(ABC):
    """
    Interface du repository pour les utilisateurs
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """Sauvegarder un utilisateur"""
        pass

    @abstractmethod
    def find_all(self) -> list[User]:
        """Trouver tous les utilisateurs"""
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        """Trouver un utilisateur par son id"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Mettre à jour un utilisateur"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Supprimer un utilisateur"""
        pass

    @abstractmethod
    def verify(self, id: UUID) -> User:
        """Vérifier un utilisateur"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Trouver un utilisateur par son email"""
        pass
