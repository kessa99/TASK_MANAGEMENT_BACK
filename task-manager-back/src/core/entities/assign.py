"""
Entité Assign (assignation de tâche)
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Assign:
    """
    Entité représentant l'assignation d'une tâche à un utilisateur
    """
    id: UUID
    task_id: UUID
    user_id: UUID
