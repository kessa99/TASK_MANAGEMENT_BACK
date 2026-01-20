"""
Use Case: Récupérer tous les utilisateurs
"""

from core.useCase.base import UseCase
from core.dto.user_dto import UserResponseDTO
from core.repositories.user_repository import UserRepository
from interface.http.mappers.user_mapper import map_user_entity_to_response


class GetAllUsersUseCase(UseCase[None, list[UserResponseDTO]]):
    """
    Use Case pour récupérer tous les utilisateurs
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, input_dto: None = None) -> list[UserResponseDTO]:
        """
        Récupérer tous les utilisateurs

        Returns:
            Liste des utilisateurs
        """
        users = self.user_repository.find_all()
        return [map_user_entity_to_response(user) for user in users]
