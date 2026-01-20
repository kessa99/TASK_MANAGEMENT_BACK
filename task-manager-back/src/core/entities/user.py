"""
Entités de la base de données user
"""

from uuid import UUID
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class UserRole(str, Enum):
    """
    Rôle de l'utilisateur
    """
    OWNER = "owner"
    MEMBER = "member"

@dataclass
class User:
    """
    Entité de la base de données
    """
    id: UUID
    first_name: str
    last_name: str
    email: str
    password: str
    verified: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
