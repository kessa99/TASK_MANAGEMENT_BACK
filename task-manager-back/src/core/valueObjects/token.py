"""
Value Object pour Token (JWT ou invitation)
"""

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from core.errors.base import ValidationError


@dataclass(frozen=True)
class Token:
    """
    Value Object représentant un token

    Attributes:
        value: La valeur du token
        expires_at: Date d'expiration (optionnel)

    Raises:
        ValidationError: Si le token est invalide
    """
    value: str
    expires_at: datetime | None = None

    def __post_init__(self):
        """Validation à la création"""
        if not self.value:
            raise ValidationError(
                message="Le token est requis",
                code="TOKEN_REQUIRED",
                field="token"
            )

        if len(self.value) < 16:
            raise ValidationError(
                message="Token trop court",
                code="TOKEN_TOO_SHORT",
                field="token"
            )

    def __str__(self) -> str:
        """Afficher partiellement le token pour la sécurité"""
        if len(self.value) > 8:
            return f"{self.value[:4]}...{self.value[-4:]}"
        return "****"

    @property
    def is_expired(self) -> bool:
        """Vérifier si le token est expiré"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Vérifier si le token est valide (non expiré)"""
        return not self.is_expired

    @property
    def time_remaining(self) -> timedelta | None:
        """Temps restant avant expiration"""
        if self.expires_at is None:
            return None
        remaining = self.expires_at - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)

    @classmethod
    def generate(cls, length: int = 32, expires_in: timedelta | None = None) -> "Token":
        """
        Générer un nouveau token aléatoire

        Args:
            length: Longueur du token en bytes (sera encodé en URL-safe base64)
            expires_in: Durée de validité du token

        Returns:
            Un nouveau Token
        """
        value = secrets.token_urlsafe(length)
        expires_at = None
        if expires_in:
            expires_at = datetime.utcnow() + expires_in
        return cls(value=value, expires_at=expires_at)

    @classmethod
    def from_string(cls, value: str, expires_at: datetime | None = None) -> "Token":
        """Créer un Token à partir d'une chaîne"""
        return cls(value=value, expires_at=expires_at)
