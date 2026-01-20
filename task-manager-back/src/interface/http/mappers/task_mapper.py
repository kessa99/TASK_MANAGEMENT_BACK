"""
Mappers HTTP pour Task (Entity <-> DTO)
"""

from uuid import uuid4
from datetime import datetime
from core.entities.task import Task, TaskStatus, TaskPriority
from core.dto.task_dto import TaskCreateDTO, TaskResponseDTO


def map_task_entity_to_response(task: Task) -> TaskResponseDTO:
    """Convertir une entité Task en DTO de réponse"""
    return TaskResponseDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        start_date=task.start_date,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def map_task_create_dto_to_entity(dto: TaskCreateDTO) -> Task:
    """Convertir un DTO de création en entité Task"""
    now = datetime.now()
    return Task(
        id=uuid4(),
        title=dto.title,
        description=dto.description,
        status=dto.status,
        priority=dto.priority,
        start_date=dto.start_date,
        due_date=dto.due_date,
        assigned_to=dto.assigned_to,
        created_at=now,
        updated_at=now,
    )
