"""
Mappers pour Invitation
"""

from core.entities.invitation import Invitation
from infrastructure.database.models.invitationModel import InvitationModel


def map_invitation_model_to_entity(invitation_model: InvitationModel) -> Invitation:
    """Mappage d'un modèle InvitationModel vers une entité Invitation"""
    return Invitation(
        id=invitation_model.id,
        email=invitation_model.email,
        task_id=invitation_model.task_id,
        token=invitation_model.token,
        invited_by=invitation_model.invited_by,
        accepted=invitation_model.accepted,
        expires_at=invitation_model.expires_at,
        created_at=invitation_model.created_at,
    )


def map_entity_to_invitation_model(entity: Invitation) -> InvitationModel:
    """Mappage d'une entité Invitation vers un modèle InvitationModel"""
    return InvitationModel(
        id=entity.id,
        email=entity.email,
        task_id=entity.task_id,
        token=entity.token,
        invited_by=entity.invited_by,
        accepted=entity.accepted,
        expires_at=entity.expires_at,
        created_at=entity.created_at,
    )
