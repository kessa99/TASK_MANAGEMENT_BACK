"""
Controller pour les invitations
"""

import secrets
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.dto.invitation_dto import (
    InviteCreateDTO,
    InviteAcceptDTO,
    InvitationResponseDTO,
    InvitationDetailDTO,
)
from core.dto.auth_dto import TokenDTO
from core.entities.invitation import Invitation
from core.entities.user import User, UserRole
from core.entities.assign import Assign
from core.services.auth_service import AuthService
from infrastructure.database.repository.invitation_repository import InvitationRepositoryImpl
from infrastructure.database.repository.user_repository import UserRepositoryImpl
from infrastructure.database.repository.task_repository import TaskRepositoryImpl
from infrastructure.database.repository.assign_repository import AssignRepositoryImpl
from infrastructure.external.email_service import EmailService
from interface.http.mappers.invitation_mapper import (
    map_invitation_entity_to_response,
    map_invitation_entity_to_detail,
)


class InvitationController:
    """Controller pour les opérations d'invitation"""

    def __init__(self, db: Session):
        self.db = db
        self.invitation_repo = InvitationRepositoryImpl(db)
        self.user_repo = UserRepositoryImpl(db)
        self.task_repo = TaskRepositoryImpl(db)
        self.assign_repo = AssignRepositoryImpl(db)
        self.email_service = EmailService()

    def create_invitation(
        self,
        dto: InviteCreateDTO,
        current_user: User
    ) -> InvitationResponseDTO | str:
        """
        Créer une invitation

        Returns:
            InvitationResponseDTO si succès, str avec message d'erreur sinon
        """
        # Vérifier que la tâche existe
        task = self.task_repo.find_by_id(dto.task_id)
        if task is None:
            return "Tâche non trouvée"

        # Vérifier si l'utilisateur existe déjà
        existing_user = self.user_repo.find_by_email(dto.email)
        if existing_user is not None:
            return "Un utilisateur avec cet email existe déjà. Assignez-le directement à la tâche."

        # Vérifier s'il y a déjà une invitation en attente pour cet email et cette tâche
        existing_invitations = self.invitation_repo.find_by_email(dto.email)
        for inv in existing_invitations:
            if inv.task_id == dto.task_id and inv.is_valid():
                return "Une invitation est déjà en attente pour cet email et cette tâche"

        # Générer un token unique
        token = secrets.token_urlsafe(32)

        # Créer l'invitation
        now = datetime.utcnow()
        invitation = Invitation(
            id=uuid4(),
            email=dto.email,
            task_id=dto.task_id,
            token=token,
            invited_by=current_user.id,
            accepted=False,
            expires_at=now + timedelta(days=7),
            created_at=now,
        )

        saved_invitation = self.invitation_repo.save(invitation)

        # Envoyer l'email d'invitation
        inviter_name = f"{current_user.first_name} {current_user.last_name}"
        self.email_service.send_invitation_email(
            to_email=dto.email,
            inviter_name=inviter_name,
            task_title=task.title,
            invitation_token=token,
        )

        return map_invitation_entity_to_response(saved_invitation)

    def get_all_pending(self) -> list[InvitationDetailDTO]:
        """Récupérer toutes les invitations en attente avec détails"""
        invitations = self.invitation_repo.find_pending()
        result = []

        for inv in invitations:
            task = self.task_repo.find_by_id(inv.task_id)
            inviter = self.user_repo.find_by_id(inv.invited_by)

            task_title = task.title if task else "Tâche supprimée"
            inviter_name = f"{inviter.first_name} {inviter.last_name}" if inviter else "Utilisateur supprimé"

            result.append(map_invitation_entity_to_detail(inv, task_title, inviter_name))

        return result

    def get_by_id(self, id) -> InvitationDetailDTO | None:
        """Récupérer une invitation par son ID avec détails"""
        invitation = self.invitation_repo.find_by_id(id)
        if invitation is None:
            return None

        task = self.task_repo.find_by_id(invitation.task_id)
        inviter = self.user_repo.find_by_id(invitation.invited_by)

        task_title = task.title if task else "Tâche supprimée"
        inviter_name = f"{inviter.first_name} {inviter.last_name}" if inviter else "Utilisateur supprimé"

        return map_invitation_entity_to_detail(invitation, task_title, inviter_name)

    def get_by_token(self, token: str) -> InvitationDetailDTO | None:
        """Récupérer une invitation par son token avec détails"""
        invitation = self.invitation_repo.find_by_token(token)
        if invitation is None:
            return None

        task = self.task_repo.find_by_id(invitation.task_id)
        inviter = self.user_repo.find_by_id(invitation.invited_by)

        task_title = task.title if task else "Tâche supprimée"
        inviter_name = f"{inviter.first_name} {inviter.last_name}" if inviter else "Utilisateur supprimé"

        return map_invitation_entity_to_detail(invitation, task_title, inviter_name)

    def accept_invitation(self, dto: InviteAcceptDTO) -> TokenDTO | str:
        """
        Accepter une invitation: créer le compte et assigner la tâche

        Returns:
            TokenDTO si succès, str avec message d'erreur sinon
        """
        # Trouver l'invitation par token
        invitation = self.invitation_repo.find_by_token(dto.token)
        if invitation is None:
            return "Invitation non trouvée"

        # Vérifier si l'invitation est valide
        if invitation.accepted:
            return "Cette invitation a déjà été acceptée"

        if invitation.is_expired():
            return "Cette invitation a expiré"

        # Vérifier que l'email n'est pas déjà utilisé
        existing_user = self.user_repo.find_by_email(invitation.email)
        if existing_user is not None:
            return "Un compte existe déjà avec cet email"

        # Créer le nouvel utilisateur
        now = datetime.utcnow()
        new_user = User(
            id=uuid4(),
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=invitation.email,
            password=AuthService.hash_password(dto.password),
            verified=True,  # Vérifié car invité par un OWNER
            role=UserRole.MEMBER,
            created_at=now,
            updated_at=now,
        )

        saved_user = self.user_repo.save(new_user)

        # Créer l'assignation à la tâche
        assign = Assign(
            id=uuid4(),
            task_id=invitation.task_id,
            user_id=saved_user.id,
        )
        self.assign_repo.save(assign)

        # Marquer l'invitation comme acceptée
        invitation.accepted = True
        self.invitation_repo.update(invitation)

        # Envoyer l'email de bienvenue
        self.email_service.send_welcome_email(
            to_email=saved_user.email,
            first_name=saved_user.first_name,
        )

        # Générer les tokens pour connexion automatique
        access_token = AuthService.create_access_token(saved_user)
        refresh_token = AuthService.create_refresh_token(saved_user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def delete(self, id) -> bool:
        """Supprimer/Annuler une invitation"""
        invitation = self.invitation_repo.find_by_id(id)
        if invitation is None:
            return False
        self.invitation_repo.delete(id)
        return True

    def resend_invitation(self, id, current_user: User) -> bool:
        """Renvoyer l'email d'invitation"""
        invitation = self.invitation_repo.find_by_id(id)
        if invitation is None:
            return False

        if invitation.accepted:
            return False

        task = self.task_repo.find_by_id(invitation.task_id)
        if task is None:
            return False

        inviter_name = f"{current_user.first_name} {current_user.last_name}"
        self.email_service.send_invitation_email(
            to_email=invitation.email,
            inviter_name=inviter_name,
            task_title=task.title,
            invitation_token=invitation.token,
        )

        return True
