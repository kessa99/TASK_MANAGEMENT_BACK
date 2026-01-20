"""
Use Case: Rafraîchir le token d'accès
"""

from core.useCase.base import UseCase
from core.dto.auth_dto import RefreshTokenDTO, TokenDTO
from core.repositories.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.errors.base import AuthenticationError
from core.errors.user_errors import UserNotFoundError


class RefreshTokenUseCase(UseCase[RefreshTokenDTO, TokenDTO]):
    """
    Use Case pour rafraîchir le token d'accès

    Règles métier:
    - Le refresh token doit être valide
    - Le refresh token ne doit pas être expiré
    - L'utilisateur doit exister
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, input_dto: RefreshTokenDTO) -> TokenDTO:
        """
        Rafraîchir le token d'accès

        Args:
            input_dto: Le refresh token

        Returns:
            TokenDTO: Les nouveaux tokens

        Raises:
            AuthenticationError: Si le refresh token est invalide
            UserNotFoundError: Si l'utilisateur n'existe plus
        """
        # Vérifier que c'est bien un refresh token
        if not AuthService.is_refresh_token(input_dto.refresh_token):
            raise AuthenticationError(
                message="Token invalide",
                code="INVALID_TOKEN_TYPE"
            )

        # Vérifier si le token est expiré
        if AuthService.is_token_expired(input_dto.refresh_token):
            raise AuthenticationError(
                message="Refresh token expiré",
                code="TOKEN_EXPIRED"
            )

        # Récupérer l'ID utilisateur du token
        user_id = AuthService.get_user_id_from_token(input_dto.refresh_token)
        if user_id is None:
            raise AuthenticationError(
                message="Token invalide",
                code="INVALID_TOKEN"
            )

        # Trouver l'utilisateur
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        # Générer de nouveaux tokens
        access_token = AuthService.create_access_token(user)
        refresh_token = AuthService.create_refresh_token(user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )
