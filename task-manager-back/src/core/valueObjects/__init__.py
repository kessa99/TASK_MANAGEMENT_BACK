"""
Value Objects - Objets immuables avec validation intégrée
"""

from core.valueObjects.email import Email
from core.valueObjects.password import Password
from core.valueObjects.token import Token

__all__ = ["Email", "Password", "Token"]
