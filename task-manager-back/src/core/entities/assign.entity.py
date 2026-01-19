"""
Entités de la base de données assign
"""

from dataclasses import dataclass

@dataclass
class Assign:
    """
    Entité de la base de données
    """
    id: int
    task_id: int
    user_id: int
