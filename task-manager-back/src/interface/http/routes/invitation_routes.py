"""
Routes pour les invitations
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.invitation_dto import (
    InviteCreateDTO,
    InviteAcceptDTO,
    InvitationResponseDTO,
    InvitationDetailDTO,
)
from core.dto.auth_dto import TokenDTO
from core.entities.user import User
from interface.http.controllers.invitation_controller import InvitationController
from interface.http.depenencies.db import get_db
from interface.http.depenencies.auth import get_current_owner

router = APIRouter(prefix="/invitations", tags=["Invitations"])


@router.post("", response_model=InvitationResponseDTO, status_code=status.HTTP_201_CREATED)
def create_invitation(
    dto: InviteCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """
    Inviter un utilisateur par email et l'assigner à une tâche (OWNER uniquement)

    Le destinataire recevra un email avec un lien pour créer son compte
    et sera automatiquement assigné à la tâche spécifiée.
    """
    controller = InvitationController(db)
    result = controller.create_invitation(dto, current_user)

    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result
        )

    return result


@router.get("", response_model=list[InvitationDetailDTO])
def get_all_pending_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Récupérer toutes les invitations en attente (OWNER uniquement)"""
    controller = InvitationController(db)
    return controller.get_all_pending()


@router.get("/check/{token}", response_model=InvitationDetailDTO)
def check_invitation_by_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Vérifier une invitation par son token (public)

    Permet au frontend d'afficher les détails de l'invitation
    avant que l'utilisateur ne crée son compte.
    """
    controller = InvitationController(db)
    invitation = controller.get_by_token(token)

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée ou invalide"
        )

    return invitation


@router.post("/accept", response_model=TokenDTO)
def accept_invitation(
    dto: InviteAcceptDTO,
    db: Session = Depends(get_db)
):
    """
    Accepter une invitation et créer son compte (public)

    Cette route permet à l'invité de:
    1. Créer son compte avec les informations fournies
    2. Être automatiquement assigné à la tâche
    3. Recevoir un token JWT pour se connecter immédiatement
    """
    controller = InvitationController(db)
    result = controller.accept_invitation(dto)

    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result
        )

    return result


@router.get("/{id}", response_model=InvitationDetailDTO)
def get_invitation_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Récupérer une invitation par son ID (OWNER uniquement)"""
    controller = InvitationController(db)
    invitation = controller.get_by_id(id)

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée"
        )

    return invitation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invitation(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Annuler/Supprimer une invitation (OWNER uniquement)"""
    controller = InvitationController(db)
    deleted = controller.delete(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation non trouvée"
        )


@router.post("/{id}/resend", status_code=status.HTTP_200_OK)
def resend_invitation(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Renvoyer l'email d'invitation (OWNER uniquement)"""
    controller = InvitationController(db)
    success = controller.resend_invitation(id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de renvoyer l'invitation"
        )

    return {"message": "Invitation renvoyée avec succès"}
