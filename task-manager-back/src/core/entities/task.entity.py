"""
Entités de la base de données
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

class TaskStatus(str, Enum):
    """
    État de la tâche
    """
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskPriority(str, Enum):
    """
    Priorité de la tâche
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass
class Task:
    """
    Entité de la base de données
    """
    id: UUID
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    start_date: datetime | None
    due_date: datetime | None
    assigned_to: List[UUID]
    created_at: datetime
    updated_at: datetime
