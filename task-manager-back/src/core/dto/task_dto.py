"""
DTOs pour Task
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from core.entities.task import TaskStatus, TaskPriority


class TaskCreateDTO(BaseModel):
    """DTO pour créer une tâche"""
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    start_date: datetime | None = None
    due_date: datetime | None = None
    assigned_to: list[UUID] = []


class TaskUpdateDTO(BaseModel):
    """DTO pour mettre à jour une tâche"""
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    assigned_to: list[UUID] | None = None


class TaskResponseDTO(BaseModel):
    """DTO pour la réponse tâche"""
    id: UUID
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    start_date: datetime | None
    due_date: datetime | None
    assigned_to: list[UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
