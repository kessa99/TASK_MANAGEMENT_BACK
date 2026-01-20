"""
Value Object pour Password
"""

import re
from dataclasses import dataclass
from core.errors.base import ValidationError


@dataclass(frozen=True)
class Password:
    """
    Value Object représentant un mot de passe valide (avant hashage)

    Règles de validation:
    - Minimum 8 caractères
    - Au moins une lettre majuscule
    - Au moins une lettre minuscule
    - Au moins un chiffre

    Attributes:
        value: Le mot de passe en clair

    Raises:
        ValidationError: Si le mot de passe ne respecte pas les règles
    """
    value: str

    # Configuration des règles (peut être modifiée)
    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 128
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_DIGIT: bool = True
    REQUIRE_SPECIAL: bool = False

    def __post_init__(self):
        """Validation à la création"""
        errors = []

        if not self.value:
            raise ValidationError(
                message="Le mot de passe est requis",
                code="PASSWORD_REQUIRED",
                field="password"
            )

        # Longueur minimale
        if len(self.value) < self.MIN_LENGTH:
            errors.append(f"au moins {self.MIN_LENGTH} caractères")

        # Longueur maximale
        if len(self.value) > self.MAX_LENGTH:
            raise ValidationError(
                message=f"Le mot de passe ne peut pas dépasser {self.MAX_LENGTH} caractères",
                code="PASSWORD_TOO_LONG",
                field="password"
            )

        # Majuscule
        if self.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', self.value):
            errors.append("une lettre majuscule")

        # Minuscule
        if self.REQUIRE_LOWERCASE and not re.search(r'[a-z]', self.value):
            errors.append("une lettre minuscule")

        # Chiffre
        if self.REQUIRE_DIGIT and not re.search(r'\d', self.value):
            errors.append("un chiffre")

        # Caractère spécial
        if self.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.value):
            errors.append("un caractère spécial")

        if errors:
            raise ValidationError(
                message=f"Le mot de passe doit contenir {', '.join(errors)}",
                code="PASSWORD_WEAK",
                field="password"
            )

    def __str__(self) -> str:
        """Ne jamais afficher le mot de passe en clair"""
        return "********"

    def __repr__(self) -> str:
        return "Password(****)"

    @property
    def strength(self) -> str:
        """Évaluer la force du mot de passe"""
        score = 0

        if len(self.value) >= 12:
            score += 2
        elif len(self.value) >= 8:
            score += 1

        if re.search(r'[A-Z]', self.value):
            score += 1
        if re.search(r'[a-z]', self.value):
            score += 1
        if re.search(r'\d', self.value):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', self.value):
            score += 2

        if score <= 2:
            return "faible"
        elif score <= 4:
            return "moyen"
        else:
            return "fort"

    @classmethod
    def from_string(cls, value: str) -> "Password":
        """Créer un Password à partir d'une chaîne"""
        return cls(value=value)
