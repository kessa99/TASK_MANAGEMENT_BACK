"""
Mappers HTTP pour Assign (Entity <-> DTO)
"""

from uuid import uuid4
from core.entities.assign import Assign
from core.dto.assign_dto import AssignCreateDTO, AssignResponseDTO


def map_assign_entity_to_response(assign: Assign) -> AssignResponseDTO:
    """Convertir une entité Assign en DTO de réponse"""
    return AssignResponseDTO(
        id=assign.id,
        task_id=assign.task_id,
        user_id=assign.user_id,
    )


def map_assign_create_dto_to_entity(dto: AssignCreateDTO) -> Assign:
    """Convertir un DTO de création en entité Assign"""
    return Assign(
        id=uuid4(),
        task_id=dto.task_id,
        user_id=dto.user_id,
    )
