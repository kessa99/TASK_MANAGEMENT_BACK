"""
Service d'authentification
"""

from datetime import datetime, timedelta
from uuid import UUID
from jose import jwt, JWTError
from passlib.context import CryptContext
from config.settings import settings
from core.entities.user import User, UserRole


# Configuration du hashage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service pour l'authentification JWT"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hasher un mot de passe"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user: User) -> str:
        """Créer un token d'accès JWT"""
        now = datetime.utcnow()
        expire = now + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "verified": user.verified,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "type": "access",
            "iat": now.timestamp(),
            "exp": expire,
        }
        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def create_refresh_token(user: User) -> str:
        """Créer un token de rafraîchissement JWT"""
        now = datetime.utcnow()
        expire = now + timedelta(
            days=settings.jwt_refresh_token_expire_days
        )
        payload = {
            "sub": str(user.id),
            "type": "refresh",
            "iat": now.timestamp(),
            "exp": expire,
        }
        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def decode_token(token: str) -> dict | None:
        """Décoder un token JWT"""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def get_user_id_from_token(token: str) -> UUID | None:
        """Extraire l'ID utilisateur du token"""
        payload = AuthService.decode_token(token)
        if payload is None:
            return None
        try:
            return UUID(payload.get("sub"))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def get_role_from_token(token: str) -> UserRole | None:
        """Extraire le rôle utilisateur du token"""
        payload = AuthService.decode_token(token)
        if payload is None:
            return None
        try:
            return UserRole(payload.get("role"))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """Vérifier si le token est expiré"""
        payload = AuthService.decode_token(token)
        if payload is None:
            return True
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.utcnow() > datetime.fromtimestamp(exp)

    @staticmethod
    def is_refresh_token(token: str) -> bool:
        """Vérifier si c'est un token de rafraîchissement"""
        payload = AuthService.decode_token(token)
        if payload is None:
            return False
        return payload.get("type") == "refresh"
