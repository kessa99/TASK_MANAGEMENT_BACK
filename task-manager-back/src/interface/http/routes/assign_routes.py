"""
Routes pour Assign (assignation de tâches)
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.assign_dto import AssignCreateDTO, AssignResponseDTO
from core.entities.user import User, UserRole
from interface.http.controllers.assign_controller import AssignController
from interface.http.dependencies.db import get_db
from interface.http.dependencies.auth import get_current_verified_user, get_current_owner

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("", response_model=AssignResponseDTO, status_code=status.HTTP_201_CREATED)
def create_assignment(
    dto: AssignCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Créer une assignation (OWNER uniquement)"""
    controller = AssignController(db)
    return controller.create(dto)


@router.get("", response_model=list[AssignResponseDTO])
def get_all_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Récupérer toutes les assignations (OWNER uniquement)"""
    controller = AssignController(db)
    return controller.get_all()


@router.get("/my", response_model=list[AssignResponseDTO])
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """Récupérer mes assignations"""
    controller = AssignController(db)
    return controller.get_assignments_for_user(current_user.id)


@router.get("/{id}", response_model=AssignResponseDTO)
def get_assignment_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    Récupérer une assignation par son ID
    - OWNER: peut voir toutes les assignations
    - MEMBER: peut voir uniquement ses propres assignations
    """
    controller = AssignController(db)
    assignment = controller.get_by_id(id)
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignation non trouvée"
        )

    # MEMBER ne peut voir que ses propres assignations
    if current_user.role == UserRole.MEMBER and assignment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas accès à cette assignation"
        )

    return assignment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # OWNER uniquement
):
    """Supprimer une assignation (OWNER uniquement)"""
    controller = AssignController(db)
    deleted = controller.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignation non trouvée"
        )


@router.get("/user/{user_id}", response_model=list[AssignResponseDTO])
def get_assignments_for_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    Récupérer les assignations d'un utilisateur
    - OWNER: peut voir les assignations de tout le monde
    - MEMBER: peut voir uniquement ses propres assignations
    """
    # MEMBER ne peut voir que ses propres assignations
    if current_user.role == UserRole.MEMBER and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres assignations"
        )

    controller = AssignController(db)
    return controller.get_assignments_for_user(user_id)
