"""
Value Object pour Email
"""

import re
from dataclasses import dataclass
from core.errors.base import ValidationError


@dataclass(frozen=True)
class Email:
    """
    Value Object représentant un email valide

    Attributes:
        value: L'adresse email

    Raises:
        ValidationError: Si l'email est invalide
    """
    value: str

    def __post_init__(self):
        """Validation à la création"""
        if not self.value:
            raise ValidationError(
                message="L'email est requis",
                code="EMAIL_REQUIRED",
                field="email"
            )

        # Pattern de validation email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValidationError(
                message="Format d'email invalide",
                code="EMAIL_INVALID_FORMAT",
                field="email"
            )

        # Longueur maximale
        if len(self.value) > 255:
            raise ValidationError(
                message="L'email ne peut pas dépasser 255 caractères",
                code="EMAIL_TOO_LONG",
                field="email"
            )

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self.value.lower() == other.value.lower()
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return False

    @property
    def domain(self) -> str:
        """Retourne le domaine de l'email"""
        return self.value.split("@")[1]

    @property
    def local_part(self) -> str:
        """Retourne la partie locale de l'email (avant @)"""
        return self.value.split("@")[0]

    @classmethod
    def from_string(cls, value: str) -> "Email":
        """Créer un Email à partir d'une chaîne"""
        return cls(value=value.strip().lower())
