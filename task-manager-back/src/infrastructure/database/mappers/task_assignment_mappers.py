"""
Mappers de la base de données
"""

from core.entities.assign import Assign
from infrastructure.database.models.taskAssignment import TaskAssignmentModel

def map_task_assignment_model_to_entity(task_assignment_model: TaskAssignmentModel) -> Assign:
    """
    Mappage d'un modèle de la base de données à un entité
    """
    return Assign(
        id=task_assignment_model.id,
        task_id=task_assignment_model.task_id,
        user_id=task_assignment_model.user_id,
    )

def map_entity_to_task_assignment_model(entity: Assign) -> TaskAssignmentModel:
    """
    Mappage d'une entité à un modèle de la base de données
    """
    return TaskAssignmentModel(
        id=entity.id,
        task_id=entity.task_id,
        user_id=entity.user_id,
    )
