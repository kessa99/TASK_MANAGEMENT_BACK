"""
Routes pour l'authentification
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.auth_dto import LoginDTO, RegisterDTO, TokenDTO, RefreshTokenDTO
from core.dto.user_dto import UserResponseDTO
from core.entities.user import User
from interface.http.controllers.auth_controller import AuthController
from interface.http.depenencies.db import get_db
from interface.http.depenencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def register(dto: RegisterDTO, db: Session = Depends(get_db)):
    """Inscrire un nouvel utilisateur"""
    controller = AuthController(db)
    user = controller.register(dto)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    return user


@router.post("/login", response_model=TokenDTO)
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
    return tokens


@router.post("/refresh", response_model=TokenDTO)
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
    return tokens


@router.get("/me", response_model=UserResponseDTO)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les informations de l'utilisateur connecté"""
    controller = AuthController(db)
    return controller.get_me(current_user)
