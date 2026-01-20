"""
DTOs pour Invitation
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class InviteCreateDTO(BaseModel):
    """DTO pour créer une invitation"""
    email: EmailStr
    task_id: UUID


class InviteAcceptDTO(BaseModel):
    """DTO pour accepter une invitation"""
    token: str
    first_name: str
    last_name: str
    password: str


class InvitationResponseDTO(BaseModel):
    """DTO pour la réponse invitation"""
    id: UUID
    email: str
    task_id: UUID
    invited_by: UUID
    accepted: bool
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class InvitationDetailDTO(BaseModel):
    """DTO détaillé pour une invitation (avec infos tâche)"""
    id: UUID
    email: str
    task_id: UUID
    task_title: str
    invited_by: UUID
    inviter_name: str
    accepted: bool
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
