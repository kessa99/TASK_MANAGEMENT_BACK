"""
DTOs pour Assign (assignation de tâche)
"""

from uuid import UUID
from pydantic import BaseModel


class AssignCreateDTO(BaseModel):
    """DTO pour créer une assignation"""
    task_id: UUID
    user_id: UUID


class AssignResponseDTO(BaseModel):
    """DTO pour la réponse assignation"""
    id: UUID
    task_id: UUID
    user_id: UUID

    model_config = {"from_attributes": True}
