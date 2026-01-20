"""
DTOs pour User
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from core.entities.user import UserRole


class UserCreateDTO(BaseModel):
    """DTO pour créer un utilisateur"""
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.MEMBER


class UserUpdateDTO(BaseModel):
    """DTO pour mettre à jour un utilisateur"""
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: UserRole | None = None


class UserResponseDTO(BaseModel):
    """DTO pour la réponse utilisateur"""
    id: UUID
    first_name: str
    last_name: str
    email: str
    verified: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
