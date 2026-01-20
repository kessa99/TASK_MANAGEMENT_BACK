"""
Mappers pour Task
"""

from typing import List
from uuid import UUID
from core.entities.task import Task
from infrastructure.database.models.taskModel import TaskModel


def map_task_model_to_entity(task_model: TaskModel, assigned_to: List[UUID] | None = None) -> Task:
    """
    Mappage d'un modèle TaskModel vers une entité Task
    """
    return Task(
        id=task_model.id,
        title=task_model.title,
        description=task_model.description,
        status=task_model.status,
        priority=task_model.priority,
        start_date=task_model.start_date,
        due_date=task_model.due_date,
        created_at=task_model.created_at,
        updated_at=task_model.updated_at,
        assigned_to=assigned_to or [],
    )


def map_entity_to_task_model(entity: Task) -> TaskModel:
    """
    Mappage d'une entité Task vers un modèle TaskModel
    Note: assigned_to n'est pas mappé car géré via TaskAssignment
    """
    return TaskModel(
        id=entity.id,
        title=entity.title,
        description=entity.description,
        status=entity.status,
        priority=entity.priority,
        start_date=entity.start_date,
        due_date=entity.due_date,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
