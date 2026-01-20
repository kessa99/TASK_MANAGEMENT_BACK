"""
Use Case: Accepter une invitation
"""

from uuid import uuid4
from datetime import datetime
from core.useCase.base import UseCase
from core.dto.invitation_dto import InviteAcceptDTO
from core.dto.auth_dto import TokenDTO
from core.entities.user import User, UserRole
from core.entities.assign import Assign
from core.repositories.invitation_repository import InvitationRepository
from core.repositories.user_repository import UserRepository
from core.repositories.assign_repository import AssignRepository
from core.services.auth_service import AuthService
from core.valueObjects.password import Password
from core.errors.user_errors import UserAlreadyExistsError
from core.errors.invitation_errors import (
    InvitationNotFoundError,
    InvitationExpiredError,
    InvitationAlreadyAcceptedError,
)
from infrastructure.external.email_service import EmailService


class AcceptInvitationUseCase(UseCase[InviteAcceptDTO, TokenDTO]):
    """
    Use Case pour accepter une invitation

    Règles métier:
    - L'invitation doit exister
    - L'invitation ne doit pas être expirée
    - L'invitation ne doit pas déjà être acceptée
    - Crée un nouveau compte utilisateur
    - Assigne automatiquement la tâche
    - Retourne les tokens pour connexion immédiate
    """

    def __init__(
        self,
        invitation_repository: InvitationRepository,
        user_repository: UserRepository,
        assign_repository: AssignRepository,
    ):
        self.invitation_repository = invitation_repository
        self.user_repository = user_repository
        self.assign_repository = assign_repository
        self.email_service = EmailService()

    def execute(self, input_dto: InviteAcceptDTO) -> TokenDTO:
        """
        Accepter une invitation

        Args:
            input_dto: Token et données du nouvel utilisateur

        Returns:
            TokenDTO: Les tokens d'accès pour connexion immédiate

        Raises:
            InvitationNotFoundError: Si l'invitation n'existe pas
            InvitationExpiredError: Si l'invitation est expirée
            InvitationAlreadyAcceptedError: Si l'invitation est déjà acceptée
            UserAlreadyExistsError: Si l'email est déjà utilisé
        """
        # Trouver l'invitation
        invitation = self.invitation_repository.find_by_token(input_dto.token)
        if invitation is None:
            raise InvitationNotFoundError()

        # Vérifier si déjà acceptée
        if invitation.accepted:
            raise InvitationAlreadyAcceptedError()

        # Vérifier si expirée
        if invitation.is_expired():
            raise InvitationExpiredError()

        # Vérifier que l'email n'est pas déjà utilisé
        existing_user = self.user_repository.find_by_email(invitation.email)
        if existing_user is not None:
            raise UserAlreadyExistsError()

        # Valider le mot de passe
        password = Password.from_string(input_dto.password)

        # Créer l'utilisateur
        now = datetime.utcnow()
        new_user = User(
            id=uuid4(),
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            email=invitation.email,
            password=AuthService.hash_password(password.value),
            verified=True,  # Vérifié car invité par un OWNER
            role=UserRole.MEMBER,
            created_at=now,
            updated_at=now,
        )

        saved_user = self.user_repository.save(new_user)

        # Créer l'assignation
        assign = Assign(
            id=uuid4(),
            task_id=invitation.task_id,
            user_id=saved_user.id,
        )
        self.assign_repository.save(assign)

        # Marquer l'invitation comme acceptée
        invitation.accepted = True
        self.invitation_repository.update(invitation)

        # Envoyer l'email de bienvenue
        self.email_service.send_welcome_email(
            to_email=saved_user.email,
            first_name=saved_user.first_name,
        )

        # Générer les tokens
        access_token = AuthService.create_access_token(saved_user)
        refresh_token = AuthService.create_refresh_token(saved_user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )
