"""
Core repository interface pour les invitations
"""

from abc import ABC, abstractmethod
from uuid import UUID
from core.entities.invitation import Invitation


class InvitationRepository(ABC):
    """
    Interface du repository pour les invitations
    """

    @abstractmethod
    def save(self, invitation: Invitation) -> Invitation:
        """Sauvegarder une invitation"""
        pass

    @abstractmethod
    def find_all(self) -> list[Invitation]:
        """Trouver toutes les invitations"""
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> Invitation | None:
        """Trouver une invitation par son id"""
        pass

    @abstractmethod
    def find_by_token(self, token: str) -> Invitation | None:
        """Trouver une invitation par son token"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> list[Invitation]:
        """Trouver les invitations par email"""
        pass

    @abstractmethod
    def find_pending(self) -> list[Invitation]:
        """Trouver les invitations en attente (non acceptées et non expirées)"""
        pass

    @abstractmethod
    def update(self, invitation: Invitation) -> Invitation:
        """Mettre à jour une invitation"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Supprimer une invitation"""
        pass
