"""
Use Case: Récupérer un utilisateur
"""

from uuid import UUID
from core.useCase.base import UseCase
from core.dto.user_dto import UserResponseDTO
from core.repositories.user_repository import UserRepository
from core.errors.user_errors import UserNotFoundError
from interface.http.mappers.user_mapper import map_user_entity_to_response


class GetUserUseCase(UseCase[UUID, UserResponseDTO]):
    """
    Use Case pour récupérer un utilisateur par son ID
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> UserResponseDTO:
        """
        Récupérer un utilisateur

        Args:
            user_id: L'ID de l'utilisateur

        Returns:
            UserResponseDTO: L'utilisateur

        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
        """
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        return map_user_entity_to_response(user)
