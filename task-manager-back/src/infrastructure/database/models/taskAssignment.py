"""
Modèle de la base de données TASK_ASSIGNMENT
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.database.models.base import Base
from core.entities.task import TaskStatus, TaskPriority

class TaskAssignmentModel(Base):
    """
    Modèle de la base de données TASK_ASSIGNMENT
    """

    __tablename__ = "task_assignment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=datetime.now())