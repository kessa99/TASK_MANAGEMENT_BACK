"""
Repository implementation pour les invitations
"""

from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from core.entities.invitation import Invitation
from core.repositories.invitation_repository import InvitationRepository
from infrastructure.database.models.invitationModel import InvitationModel
from infrastructure.database.mappers.invitation_mappers import (
    map_entity_to_invitation_model,
    map_invitation_model_to_entity,
)


class InvitationRepositoryImpl(InvitationRepository):
    """
    Implémentation du repository pour les invitations
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, invitation: Invitation) -> Invitation:
        """Sauvegarder une invitation"""
        invitation_model = map_entity_to_invitation_model(invitation)
        self.session.add(invitation_model)
        self.session.commit()
        self.session.refresh(invitation_model)
        return map_invitation_model_to_entity(invitation_model)

    def find_all(self) -> list[Invitation]:
        """Trouver toutes les invitations"""
        invitation_models = self.session.query(InvitationModel).all()
        return [map_invitation_model_to_entity(m) for m in invitation_models]

    def find_by_id(self, id: UUID) -> Invitation | None:
        """Trouver une invitation par son id"""
        invitation_model = self.session.query(InvitationModel).filter(
            InvitationModel.id == id
        ).first()
        if invitation_model is None:
            return None
        return map_invitation_model_to_entity(invitation_model)

    def find_by_token(self, token: str) -> Invitation | None:
        """Trouver une invitation par son token"""
        invitation_model = self.session.query(InvitationModel).filter(
            InvitationModel.token == token
        ).first()
        if invitation_model is None:
            return None
        return map_invitation_model_to_entity(invitation_model)

    def find_by_email(self, email: str) -> list[Invitation]:
        """Trouver les invitations par email"""
        invitation_models = self.session.query(InvitationModel).filter(
            InvitationModel.email == email
        ).all()
        return [map_invitation_model_to_entity(m) for m in invitation_models]

    def find_pending(self) -> list[Invitation]:
        """Trouver les invitations en attente (non acceptées et non expirées)"""
        now = datetime.utcnow()
        invitation_models = self.session.query(InvitationModel).filter(
            InvitationModel.accepted == False,
            InvitationModel.expires_at > now
        ).all()
        return [map_invitation_model_to_entity(m) for m in invitation_models]

    def update(self, invitation: Invitation) -> Invitation:
        """Mettre à jour une invitation"""
        invitation_model = self.session.query(InvitationModel).filter(
            InvitationModel.id == invitation.id
        ).first()
        invitation_model.accepted = invitation.accepted
        self.session.commit()
        return map_invitation_model_to_entity(invitation_model)

    def delete(self, id: UUID) -> None:
        """Supprimer une invitation"""
        invitation_model = self.session.query(InvitationModel).filter(
            InvitationModel.id == id
        ).first()
        if invitation_model:
            self.session.delete(invitation_model)
            self.session.commit()
