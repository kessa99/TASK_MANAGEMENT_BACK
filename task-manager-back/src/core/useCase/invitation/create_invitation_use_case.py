"""
Use Case: Créer une invitation
"""

from uuid import uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass
from core.useCase.base import UseCase
from core.dto.invitation_dto import InviteCreateDTO, InvitationResponseDTO
from core.entities.invitation import Invitation
from core.entities.user import User
from core.repositories.invitation_repository import InvitationRepository
from core.repositories.user_repository import UserRepository
from core.repositories.task_repository import TaskRepository
from core.valueObjects.email import Email
from core.valueObjects.token import Token
from core.errors.user_errors import UserAlreadyExistsError
from core.errors.task_errors import TaskNotFoundError
from core.errors.invitation_errors import InvitationAlreadyExistsError
from infrastructure.external.email_service import EmailService
from interface.http.mappers.invitation_mapper import map_invitation_entity_to_response


@dataclass
class CreateInvitationInput:
    """Input pour créer une invitation"""
    dto: InviteCreateDTO
    current_user: User


class CreateInvitationUseCase(UseCase[CreateInvitationInput, InvitationResponseDTO]):
    """
    Use Case pour créer une invitation

    Règles métier:
    - L'email ne doit pas déjà être utilisé par un utilisateur existant
    - La tâche doit exister
    - Il ne doit pas y avoir d'invitation en attente pour cet email et cette tâche
    - L'invitation expire après 7 jours
    """

    def __init__(
        self,
        invitation_repository: InvitationRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository,
    ):
        self.invitation_repository = invitation_repository
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.email_service = EmailService()

    def execute(self, input_dto: CreateInvitationInput) -> InvitationResponseDTO:
        """
        Créer une invitation

        Args:
            input_dto: Données d'invitation et utilisateur courant

        Returns:
            InvitationResponseDTO: L'invitation créée

        Raises:
            UserAlreadyExistsError: Si l'email est déjà utilisé
            TaskNotFoundError: Si la tâche n'existe pas
            InvitationAlreadyExistsError: Si une invitation existe déjà
        """
        dto = input_dto.dto
        current_user = input_dto.current_user

        # Valider l'email
        email = Email.from_string(dto.email)

        # Vérifier que la tâche existe
        task = self.task_repository.find_by_id(dto.task_id)
        if task is None:
            raise TaskNotFoundError()

        # Vérifier que l'utilisateur n'existe pas déjà
        existing_user = self.user_repository.find_by_email(email.value)
        if existing_user is not None:
            raise UserAlreadyExistsError(
                message="Un utilisateur avec cet email existe déjà. Assignez-le directement à la tâche."
            )

        # Vérifier s'il y a déjà une invitation en attente
        existing_invitations = self.invitation_repository.find_by_email(email.value)
        for inv in existing_invitations:
            if inv.task_id == dto.task_id and inv.is_valid():
                raise InvitationAlreadyExistsError()

        # Générer le token
        token = Token.generate(length=32, expires_in=timedelta(days=7))

        # Créer l'invitation
        now = datetime.utcnow()
        invitation = Invitation(
            id=uuid4(),
            email=email.value,
            task_id=dto.task_id,
            token=token.value,
            invited_by=current_user.id,
            accepted=False,
            expires_at=token.expires_at,
            created_at=now,
        )

        saved_invitation = self.invitation_repository.save(invitation)

        # Envoyer l'email
        inviter_name = f"{current_user.first_name} {current_user.last_name}"
        self.email_service.send_invitation_email(
            to_email=email.value,
            inviter_name=inviter_name,
            task_title=task.title,
            invitation_token=token.value,
        )

        return map_invitation_entity_to_response(saved_invitation)
