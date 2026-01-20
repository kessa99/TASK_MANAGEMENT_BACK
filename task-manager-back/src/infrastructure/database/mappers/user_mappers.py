"""
Mappers de la base de données
"""

from core.entities.user import User
from infrastructure.database.models.userModel import UserModel

def map_user_model_to_entity(user_model: UserModel) -> User:
    """
    Mappage d'un modèle de la base de données à un entité
    """
    return User(
        id=user_model.id,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        email=user_model.email,
        password=user_model.password,
        verified=user_model.verified,
        role=user_model.role,
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
    )

def map_entity_to_user_model(entity: User) -> UserModel:
    """
    Mappage d'une entité à un modèle de la base de données
    """
    return UserModel(
        id=entity.id,
        first_name=entity.first_name,
        last_name=entity.last_name,
        email=entity.email,
        password=entity.password,
        verified=entity.verified,
        role=entity.role,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
