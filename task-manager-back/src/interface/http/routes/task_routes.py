"""
Routes pour Task
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dto.task_dto import TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO
from core.entities.user import User, UserRole
from interface.http.controllers.task_controller import TaskController
from interface.http.dependencies.db import get_db
from interface.http.dependencies.auth import get_current_verified_user, get_current_owner

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(
    dto: TaskCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # Seul OWNER peut créer
):
    """Créer une tâche (OWNER uniquement)"""
    controller = TaskController(db)
    return controller.create(dto)


@router.get("", response_model=list[TaskResponseDTO])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    Récupérer les tâches
    - OWNER: toutes les tâches
    - MEMBER: uniquement ses tâches assignées
    """
    controller = TaskController(db)
    if current_user.role == UserRole.OWNER:
        return controller.get_all()
    else:
        return controller.get_tasks_for_user(current_user.id)


@router.get("/my", response_model=list[TaskResponseDTO])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """Récupérer mes tâches assignées"""
    controller = TaskController(db)
    return controller.get_tasks_for_user(current_user.id)


@router.get("/{id}", response_model=TaskResponseDTO)
def get_task_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    Récupérer une tâche par son ID
    - OWNER: peut voir toutes les tâches
    - MEMBER: peut voir uniquement si assigné
    """
    controller = TaskController(db)
    task = controller.get_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )

    # Vérifier l'accès pour les MEMBER
    if current_user.role == UserRole.MEMBER:
        if current_user.id not in task.assigned_to:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas accès à cette tâche"
            )

    return task


@router.put("/{id}", response_model=TaskResponseDTO)
def update_task(
    id: UUID,
    dto: TaskUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # Seul OWNER peut modifier
):
    """Mettre à jour une tâche (OWNER uniquement)"""
    controller = TaskController(db)
    task = controller.update(id, dto)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )
    return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)  # Seul OWNER peut supprimer
):
    """Supprimer une tâche (OWNER uniquement)"""
    controller = TaskController(db)
    deleted = controller.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )


@router.get("/user/{user_id}", response_model=list[TaskResponseDTO])
def get_tasks_for_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    Récupérer les tâches assignées à un utilisateur
    - OWNER: peut voir les tâches de tout le monde
    - MEMBER: peut voir uniquement ses propres tâches
    """
    # MEMBER ne peut voir que ses propres tâches
    if current_user.role == UserRole.MEMBER and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres tâches"
        )

    controller = TaskController(db)
    return controller.get_tasks_for_user(user_id)
