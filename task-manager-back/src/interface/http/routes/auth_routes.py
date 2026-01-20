"""
Routes pour l'authentification
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.auth_dto import LoginDTO, RegisterDTO, TokenDTO, RefreshTokenDTO, LogoutResponseDTO
from core.dto.user_dto import UserResponseDTO
from core.dto.response_dto import ApiResponse, success_response
from core.entities.user import User
from interface.http.controllers.auth_controller import AuthController
from interface.http.dependencies.db import get_db
from interface.http.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(dto: RegisterDTO, db: Session = Depends(get_db)):
    """Inscrire un nouvel utilisateur"""
    controller = AuthController(db)
    user = controller.register(dto)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    return success_response(data=user.model_dump(), message="Utilisateur créé avec succès")


@router.post("/login")
def login(dto: LoginDTO, db: Session = Depends(get_db)):
    """Connecter un utilisateur"""
    controller = AuthController(db)
    tokens = controller.login(dto)
    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return success_response(data=tokens.model_dump(), message="Authentification réussie")


@router.post("/refresh")
def refresh_token(dto: RefreshTokenDTO, db: Session = Depends(get_db)):
    """Rafraîchir le token d'accès"""
    controller = AuthController(db)
    tokens = controller.refresh_token(dto)
    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return success_response(data=tokens.model_dump(), message="Token rafraîchi avec succès")


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les informations de l'utilisateur connecté"""
    controller = AuthController(db)
    return success_response(data=controller.get_me(current_user).model_dump(), message="Utilisateur récupéré")


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Déconnecter l'utilisateur

    Note: Avec JWT stateless, le serveur ne peut pas invalider le token.
    Le client doit supprimer le token de son stockage local.
    Cette route sert à :
    - Confirmer la déconnexion côté API
    - Permettre l'ajout futur d'une blacklist de tokens
    """
    return success_response(data=None, message="Déconnexion réussie")
