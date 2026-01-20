"""
Dépendances d'authentification
"""

from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.entities.user import User, UserRole
from core.services.auth_service import AuthService
from infrastructure.database.repository.user_repository import UserRepositoryImpl
from interface.http.depenencies.db import get_db

# Schéma de sécurité Bearer
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance pour récupérer l'utilisateur courant depuis le token JWT
    """
    token = credentials.credentials

    # Décoder le token
    user_id = AuthService.get_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Vérifier si le token est expiré
    if AuthService.is_token_expired(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Récupérer l'utilisateur
    repository = UserRepositoryImpl(db)
    user = repository.find_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dépendance pour récupérer l'utilisateur courant vérifié
    """
    if not current_user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte non vérifié"
        )
    return current_user


async def get_current_owner(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Dépendance pour récupérer l'utilisateur courant avec le rôle OWNER
    """
    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux propriétaires"
        )
    return current_user


def require_role(allowed_roles: list[UserRole]):
    """
    Factory pour créer une dépendance qui vérifie le rôle
    """
    async def role_checker(
        current_user: User = Depends(get_current_verified_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé pour ce rôle"
            )
        return current_user
    return role_checker
