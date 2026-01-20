"""
Use Case: Inscription d'un utilisateur
"""

from uuid import uuid4
from datetime import datetime
from core.useCase.base import UseCase
from core.dto.auth_dto import RegisterDTO
from core.dto.user_dto import UserResponseDTO
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.valueObjects.email import Email
from core.valueObjects.password import Password
from core.errors.user_errors import UserAlreadyExistsError
from interface.http.mappers.user_mapper import map_user_entity_to_response


class RegisterUseCase(UseCase[RegisterDTO, UserResponseDTO]):
    """
    Use Case pour l'inscription d'un nouvel utilisateur

    Règles métier:
    - L'email doit être unique
    - L'email doit être valide
    - Le mot de passe doit respecter les règles de sécurité
    - Le mot de passe est hashé avant stockage
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, input_dto: RegisterDTO) -> UserResponseDTO:
        """
        Inscrire un nouvel utilisateur

        Args:
            input_dto: Données d'inscription

        Returns:
            UserResponseDTO: L'utilisateur créé

        Raises:
            UserAlreadyExistsError: Si l'email existe déjà
            ValidationError: Si l'email ou le mot de passe est invalide
        """
        # Valider l'email via ValueObject
        email = Email.from_string(input_dto.email)

        # Valider le mot de passe via ValueObject
        password = Password.from_string(input_dto.password)

        # Vérifier que l'email n'existe pas
        existing_user = self.user_repository.find_by_email(email.value)
        if existing_user is not None:
            raise UserAlreadyExistsError()

        # Créer l'entité User
        now = datetime.utcnow()
        user = User(
            id=uuid4(),
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            email=email.value,
            password=AuthService.hash_password(password.value),
            verified=False,
            role=input_dto.role,
            created_at=now,
            updated_at=now,
        )

        # Sauvegarder
        saved_user = self.user_repository.save(user)

        # Retourner le DTO de réponse
        return map_user_entity_to_response(saved_user)
