"""
Mappers HTTP pour Invitation (Entity <-> DTO)
"""

from core.entities.invitation import Invitation
from core.dto.invitation_dto import InvitationResponseDTO, InvitationDetailDTO


def map_invitation_entity_to_response(invitation: Invitation) -> InvitationResponseDTO:
    """Convertir une entité Invitation en DTO de réponse"""
    return InvitationResponseDTO(
        id=invitation.id,
        email=invitation.email,
        task_id=invitation.task_id,
        invited_by=invitation.invited_by,
        accepted=invitation.accepted,
        expires_at=invitation.expires_at,
        created_at=invitation.created_at,
    )


def map_invitation_entity_to_detail(
    invitation: Invitation,
    task_title: str,
    inviter_name: str
) -> InvitationDetailDTO:
    """Convertir une entité Invitation en DTO détaillé"""
    return InvitationDetailDTO(
        id=invitation.id,
        email=invitation.email,
        task_id=invitation.task_id,
        task_title=task_title,
        invited_by=invitation.invited_by,
        inviter_name=inviter_name,
        accepted=invitation.accepted,
        expires_at=invitation.expires_at,
        created_at=invitation.created_at,
    )
