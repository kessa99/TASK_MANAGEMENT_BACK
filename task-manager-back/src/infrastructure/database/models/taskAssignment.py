"""
Modèle de la base de données TASK_ASSIGNMENT
"""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.database.models.base import Base


class TaskAssignmentModel(Base):
    """
    Modèle de la base de données TASK_ASSIGNMENT
    """

    __tablename__ = "task_assignment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
