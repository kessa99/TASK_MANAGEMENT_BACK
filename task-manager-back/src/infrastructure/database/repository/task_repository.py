"""
Repository implementation pour les tasks
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.entities.task import Task
from core.repositories.task_repository import TaskRepository
from infrastructure.database.models.taskModel import TaskModel
from infrastructure.database.mappers.task_mappers import (
    map_entity_to_task_model,
    map_task_model_to_entity
)


class TaskRepositoryImpl(TaskRepository):
    """
    Implémentation du repository pour les tasks
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task) -> Task:
        """Sauvegarder une tâche"""
        task_model = map_entity_to_task_model(task)
        self.session.add(task_model)
        self.session.commit()
        return map_task_model_to_entity(task_model)

    def find_all(self) -> list[Task]:
        """Trouver toutes les tâches"""
        task_models = self.session.query(TaskModel).all()
        return [map_task_model_to_entity(task_model) for task_model in task_models]

    def find_by_id(self, id: UUID) -> Task | None:
        """Trouver une tâche par son id"""
        task_model = self.session.query(TaskModel).filter(TaskModel.id == id).first()
        if task_model is None:
            return None
        return map_task_model_to_entity(task_model)

    def update(self, task: Task) -> Task:
        """Mettre à jour une tâche"""
        task_model = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()
        task_model.title = task.title
        task_model.description = task.description
        task_model.status = task.status
        task_model.priority = task.priority
        task_model.start_date = task.start_date
        task_model.due_date = task.due_date
        self.session.commit()
        return map_task_model_to_entity(task_model)

    def delete(self, id: UUID) -> None:
        """Supprimer une tâche"""
        task_model = self.session.query(TaskModel).filter(TaskModel.id == id).first()
        if task_model:
            self.session.delete(task_model)
            self.session.commit()

    def get_tasks_for_user(self, user_id: UUID) -> list[Task]:
        """Trouver les tâches assignées à un utilisateur"""
        from infrastructure.database.models.taskAssignment import TaskAssignmentModel
        task_ids = self.session.query(TaskAssignmentModel.task_id).filter(
            TaskAssignmentModel.user_id == user_id
        ).all()
        task_ids = [t[0] for t in task_ids]
        task_models = self.session.query(TaskModel).filter(TaskModel.id.in_(task_ids)).all()
        return [map_task_model_to_entity(task_model) for task_model in task_models]
