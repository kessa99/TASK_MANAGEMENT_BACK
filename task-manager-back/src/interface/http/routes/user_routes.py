"""
Routes pour User (OWNER uniquement sauf exception)
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.user_dto import UserUpdateDTO, UserResponseDTO
from core.entities.user import User
from interface.http.controllers.user_controller import UserController
from interface.http.depenencies.db import get_db
from interface.http.depenencies.auth import get_current_owner

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponseDTO])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Récupérer tous les utilisateurs (OWNER uniquement)"""
    controller = UserController(db)
    return controller.get_all()


@router.get("/{id}", response_model=UserResponseDTO)
def get_user_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Récupérer un utilisateur par son ID (OWNER uniquement)"""
    controller = UserController(db)
    user = controller.get_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user


@router.put("/{id}", response_model=UserResponseDTO)
def update_user(
    id: UUID,
    dto: UserUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Mettre à jour un utilisateur (OWNER uniquement)"""
    controller = UserController(db)
    user = controller.update(id, dto)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Supprimer un utilisateur (OWNER uniquement)"""
    controller = UserController(db)
    deleted = controller.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )


@router.post("/{id}/verify", response_model=UserResponseDTO)
def verify_user(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Vérifier un utilisateur (OWNER uniquement)"""
    controller = UserController(db)
    user = controller.verify(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user
