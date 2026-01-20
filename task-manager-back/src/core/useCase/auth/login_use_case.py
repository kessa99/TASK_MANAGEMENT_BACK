"""
Use Case: Connexion d'un utilisateur
"""

from core.useCase.base import UseCase
from core.dto.auth_dto import LoginDTO, TokenDTO
from core.repositories.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.valueObjects.email import Email
from core.errors.user_errors import InvalidCredentialsError


class LoginUseCase(UseCase[LoginDTO, TokenDTO]):
    """
    Use Case pour la connexion d'un utilisateur

    Règles métier:
    - L'email doit exister
    - Le mot de passe doit correspondre
    - Génère un access token et un refresh token
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, input_dto: LoginDTO) -> TokenDTO:
        """
        Connecter un utilisateur

        Args:
            input_dto: Données de connexion

        Returns:
            TokenDTO: Les tokens d'accès

        Raises:
            InvalidCredentialsError: Si les identifiants sont incorrects
        """
        # Valider l'email via ValueObject
        email = Email.from_string(input_dto.email)

        # Trouver l'utilisateur
        user = self.user_repository.find_by_email(email.value)
        if user is None:
            raise InvalidCredentialsError()

        # Vérifier le mot de passe
        if not AuthService.verify_password(input_dto.password, user.password):
            raise InvalidCredentialsError()

        # Générer les tokens
        access_token = AuthService.create_access_token(user)
        refresh_token = AuthService.create_refresh_token(user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )
