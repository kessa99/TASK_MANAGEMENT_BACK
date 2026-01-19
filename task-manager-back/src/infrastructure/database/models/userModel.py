"""
Modèle de la base de données USER
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.database.models.base import Base
from core.entities.user import UserRole

class UserModel(Base):
    """
    Modèle de la base de données USER
    """

    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    verified = Column(Boolean, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=datetime.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=datetime.now())