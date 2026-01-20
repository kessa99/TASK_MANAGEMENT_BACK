"""
Modèle de la base de données TASK
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

