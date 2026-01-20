"""
Repository implementation pour les assignations
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.entities.assign import Assign
from core.repositories.assign_repository import AssignRepository
from infrastructure.database.models.taskAssignment import TaskAssignmentModel
from infrastructure.database.mappers.task_assignment_mappers import (
    map_entity_to_task_assignment_model,
    map_task_assignment_model_to_entity
)


class AssignRepositoryImpl(AssignRepository):
    """
    Implémentation du repository pour les assignations
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, assign: Assign) -> Assign:
        """Sauvegarder une assignation"""
        task_assignment_model = map_entity_to_task_assignment_model(assign)
        self.session.add(task_assignment_model)
        self.session.commit()
        return map_task_assignment_model_to_entity(task_assignment_model)

    def find_all(self) -> list[Assign]:
        """Trouver toutes les assignations"""
        task_assignment_models = self.session.query(TaskAssignmentModel).all()
        return [map_task_assignment_model_to_entity(m) for m in task_assignment_models]

    def find_by_id(self, id: UUID) -> Assign | None:
        """Trouver une assignation par son id"""
        task_assignment_model = self.session.query(TaskAssignmentModel).filter(
            TaskAssignmentModel.id == id
        ).first()
        if task_assignment_model is None:
            return None
        return map_task_assignment_model_to_entity(task_assignment_model)

    def update(self, assign: Assign) -> Assign:
        """Mettre à jour une assignation"""
        task_assignment_model = self.session.query(TaskAssignmentModel).filter(
            TaskAssignmentModel.id == assign.id
        ).first()
        task_assignment_model.task_id = assign.task_id
        task_assignment_model.user_id = assign.user_id
        self.session.commit()
        return map_task_assignment_model_to_entity(task_assignment_model)

    def delete(self, id: UUID) -> None:
        """Supprimer une assignation"""
        task_assignment_model = self.session.query(TaskAssignmentModel).filter(
            TaskAssignmentModel.id == id
        ).first()
        if task_assignment_model:
            self.session.delete(task_assignment_model)
            self.session.commit()

    def get_assignments_for_user(self, user_id: UUID) -> list[Assign]:
        """Trouver les assignations d'un utilisateur"""
        task_assignment_models = self.session.query(TaskAssignmentModel).filter(
            TaskAssignmentModel.user_id == user_id
        ).all()
        return [map_task_assignment_model_to_entity(m) for m in task_assignment_models]
