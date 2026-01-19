"""
Modèle de la base de données TASK
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.database.models.base import Base
from core.entities.task import TaskStatus, TaskPriority

class TaskModel(Base):
    """
    Modèle de la base de données TASK
    """

    __tablename__ = "task"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)
    priority = Column(Enum(TaskPriority), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    assigned_to = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=datetime.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=datetime.now())
    