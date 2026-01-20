"""
Mappers HTTP pour User (Entity <-> DTO)
"""

from uuid import uuid4
from datetime import datetime
from core.entities.user import User
from core.dto.user_dto import UserCreateDTO, UserResponseDTO


def map_user_entity_to_response(user: User) -> UserResponseDTO:
    """Convertir une entité User en DTO de réponse"""
    return UserResponseDTO(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        verified=user.verified,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def map_user_create_dto_to_entity(dto: UserCreateDTO) -> User:
    """Convertir un DTO de création en entité User"""
    now = datetime.now()
    return User(
        id=uuid4(),
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        password=dto.password,  # Note: hasher le password dans le use case
        verified=False,
        role=dto.role,
        created_at=now,
        updated_at=now,
    )
