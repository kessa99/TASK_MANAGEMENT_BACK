"""
Modèle de la base de données INVITATION
"""

import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from infrastructure.database.models.base import Base


def default_expiration():
    """Expiration par défaut : 7 jours"""
    return datetime.utcnow() + timedelta(days=7)


class InvitationModel(Base):
    """
    Modèle de la base de données INVITATION
    """

    __tablename__ = "invitation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    invited_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    accepted = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True), default=default_expiration, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
