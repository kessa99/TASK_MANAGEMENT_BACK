"""
Controller pour User
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.dto.user_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from core.entities.user import User
from infrastructure.database.repository.user_repository import UserRepositoryImpl
from interface.http.mappers.user_mapper import (
    map_user_create_dto_to_entity,
    map_user_entity_to_response,
)


class UserController:
    """Controller pour les opérations User"""

    def __init__(self, db: Session):
        self.repository = UserRepositoryImpl(db)

    def create(self, dto: UserCreateDTO) -> UserResponseDTO:
        """Créer un utilisateur"""
        entity = map_user_create_dto_to_entity(dto)
        saved_entity = self.repository.save(entity)
        return map_user_entity_to_response(saved_entity)

    def get_all(self) -> list[UserResponseDTO]:
        """Récupérer tous les utilisateurs"""
        entities = self.repository.find_all()
        return [map_user_entity_to_response(e) for e in entities]

    def get_by_id(self, id: UUID) -> UserResponseDTO | None:
        """Récupérer un utilisateur par son ID"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None
        return map_user_entity_to_response(entity)

    def update(self, id: UUID, dto: UserUpdateDTO) -> UserResponseDTO | None:
        """Mettre à jour un utilisateur"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None

        if dto.first_name is not None:
            entity.first_name = dto.first_name
        if dto.last_name is not None:
            entity.last_name = dto.last_name
        if dto.email is not None:
            entity.email = dto.email
        if dto.password is not None:
            entity.password = dto.password
        if dto.role is not None:
            entity.role = dto.role

        updated_entity = self.repository.update(entity)
        return map_user_entity_to_response(updated_entity)

    def delete(self, id: UUID) -> bool:
        """Supprimer un utilisateur"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return False
        self.repository.delete(id)
        return True

    def verify(self, id: UUID) -> UserResponseDTO | None:
        """Vérifier un utilisateur"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None
        verified_entity = self.repository.verify(id)
        return map_user_entity_to_response(verified_entity)
