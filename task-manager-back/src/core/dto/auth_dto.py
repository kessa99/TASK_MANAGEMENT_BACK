"""
DTOs pour l'authentification
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from core.entities.user import UserRole


class LoginDTO(BaseModel):
    """DTO pour la connexion"""
    email: EmailStr
    password: str


class RegisterDTO(BaseModel):
    """DTO pour l'inscription"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.MEMBER


class TokenDTO(BaseModel):
    """DTO pour la réponse avec tokens JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(default=1800, description="Durée de validité en secondes")


class TokenPayloadDTO(BaseModel):
    """
    DTO pour le payload du token JWT

    Contenu du token décodé:
    - sub: ID de l'utilisateur (subject)
    - email: Email de l'utilisateur
    - role: Rôle (owner/member)
    - verified: Compte vérifié ou non
    - type: Type de token (access/refresh)
    - iat: Date de création (issued at)
    - exp: Date d'expiration
    """
    sub: UUID  # user_id
    email: str
    role: UserRole
    verified: bool
    type: str  # "access" ou "refresh"
    iat: datetime  # issued at
    exp: datetime  # expiration

    model_config = {"from_attributes": True}


class AccessTokenPayloadDTO(BaseModel):
    """Payload spécifique au token d'accès"""
    sub: UUID
    email: str
    role: UserRole
    verified: bool
    first_name: str
    last_name: str
    type: str = "access"
    iat: datetime
    exp: datetime


class RefreshTokenPayloadDTO(BaseModel):
    """Payload spécifique au refresh token (minimal)"""
    sub: UUID
    type: str = "refresh"
    iat: datetime
    exp: datetime


class RefreshTokenDTO(BaseModel):
    """DTO pour rafraîchir le token"""
    refresh_token: str


class AuthenticatedUserDTO(BaseModel):
    """DTO représentant l'utilisateur authentifié (extrait du token)"""
    id: UUID
    email: str
    role: UserRole
    verified: bool
    first_name: str | None = None
    last_name: str | None = None
