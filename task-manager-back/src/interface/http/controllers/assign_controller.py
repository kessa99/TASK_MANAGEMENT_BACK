"""
Controller pour Assign
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.dto.assign_dto import AssignCreateDTO, AssignResponseDTO
from infrastructure.database.repository.assign_repository import AssignRepositoryImpl
from interface.http.mappers.assign_mapper import (
    map_assign_create_dto_to_entity,
    map_assign_entity_to_response,
)


class AssignController:
    """Controller pour les opérations Assign"""

    def __init__(self, db: Session):
        self.repository = AssignRepositoryImpl(db)

    def create(self, dto: AssignCreateDTO) -> AssignResponseDTO:
        """Créer une assignation"""
        entity = map_assign_create_dto_to_entity(dto)
        saved_entity = self.repository.save(entity)
        return map_assign_entity_to_response(saved_entity)

    def get_all(self) -> list[AssignResponseDTO]:
        """Récupérer toutes les assignations"""
        entities = self.repository.find_all()
        return [map_assign_entity_to_response(e) for e in entities]

    def get_by_id(self, id: UUID) -> AssignResponseDTO | None:
        """Récupérer une assignation par son ID"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None
        return map_assign_entity_to_response(entity)

    def delete(self, id: UUID) -> bool:
        """Supprimer une assignation"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return False
        self.repository.delete(id)
        return True

    def get_assignments_for_user(self, user_id: UUID) -> list[AssignResponseDTO]:
        """Récupérer les assignations d'un utilisateur"""
        entities = self.repository.get_assignments_for_user(user_id)
        return [map_assign_entity_to_response(e) for e in entities]
