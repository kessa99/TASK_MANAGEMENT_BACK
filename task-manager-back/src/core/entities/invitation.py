"""
Entité Invitation
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Invitation:
    """
    Entité représentant une invitation à rejoindre une tâche
    """
    id: UUID
    email: str
    task_id: UUID
    token: str
    invited_by: UUID
    accepted: bool
    expires_at: datetime
    created_at: datetime

    def is_expired(self) -> bool:
        """Vérifier si l'invitation est expirée"""
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        """Vérifier si l'invitation est valide (non acceptée et non expirée)"""
        return not self.accepted and not self.is_expired()
