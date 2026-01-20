"""
Controller pour Task
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.dto.task_dto import TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO
from infrastructure.database.repository.task_repository import TaskRepositoryImpl
from interface.http.mappers.task_mapper import (
    map_task_create_dto_to_entity,
    map_task_entity_to_response,
)


class TaskController:
    """Controller pour les opérations Task"""

    def __init__(self, db: Session):
        self.repository = TaskRepositoryImpl(db)

    def create(self, dto: TaskCreateDTO) -> TaskResponseDTO:
        """Créer une tâche"""
        entity = map_task_create_dto_to_entity(dto)
        saved_entity = self.repository.save(entity)
        return map_task_entity_to_response(saved_entity)

    def get_all(self) -> list[TaskResponseDTO]:
        """Récupérer toutes les tâches"""
        entities = self.repository.find_all()
        return [map_task_entity_to_response(e) for e in entities]

    def get_by_id(self, id: UUID) -> TaskResponseDTO | None:
        """Récupérer une tâche par son ID"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None
        return map_task_entity_to_response(entity)

    def update(self, id: UUID, dto: TaskUpdateDTO) -> TaskResponseDTO | None:
        """Mettre à jour une tâche"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return None

        if dto.title is not None:
            entity.title = dto.title
        if dto.description is not None:
            entity.description = dto.description
        if dto.status is not None:
            entity.status = dto.status
        if dto.priority is not None:
            entity.priority = dto.priority
        if dto.start_date is not None:
            entity.start_date = dto.start_date
        if dto.due_date is not None:
            entity.due_date = dto.due_date

        updated_entity = self.repository.update(entity)
        return map_task_entity_to_response(updated_entity)

    def delete(self, id: UUID) -> bool:
        """Supprimer une tâche"""
        entity = self.repository.find_by_id(id)
        if entity is None:
            return False
        self.repository.delete(id)
        return True

    def get_tasks_for_user(self, user_id: UUID) -> list[TaskResponseDTO]:
        """Récupérer les tâches assignées à un utilisateur"""
        entities = self.repository.get_tasks_for_user(user_id)
        return [map_task_entity_to_response(e) for e in entities]
