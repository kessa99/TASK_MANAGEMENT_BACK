"""
Repository implementation pour les users
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from infrastructure.database.models.userModel import UserModel
from infrastructure.database.mappers.user_mappers import (
    map_entity_to_user_model,
    map_user_model_to_entity
)


class UserRepositoryImpl(UserRepository):
    """
    Implémentation du repository pour les users
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        """Sauvegarder un utilisateur"""
        user_model = map_entity_to_user_model(user)
        self.session.add(user_model)
        self.session.commit()
        return map_user_model_to_entity(user_model)

    def find_all(self) -> list[User]:
        """Trouver tous les utilisateurs"""
        user_models = self.session.query(UserModel).all()
        return [map_user_model_to_entity(user_model) for user_model in user_models]

    def find_by_id(self, id: UUID) -> User | None:
        """Trouver un utilisateur par son id"""
        user_model = self.session.query(UserModel).filter(UserModel.id == id).first()
        if user_model is None:
            return None
        return map_user_model_to_entity(user_model)

    def update(self, user: User) -> User:
        """Mettre à jour un utilisateur"""
        user_model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.email = user.email
        user_model.password = user.password
        user_model.verified = user.verified
        user_model.role = user.role
        self.session.commit()
        return map_user_model_to_entity(user_model)

    def delete(self, id: UUID) -> None:
        """Supprimer un utilisateur"""
        user_model = self.session.query(UserModel).filter(UserModel.id == id).first()
        if user_model:
            self.session.delete(user_model)
            self.session.commit()

    def verify(self, id: UUID) -> User:
        """Vérifier un utilisateur"""
        user_model = self.session.query(UserModel).filter(UserModel.id == id).first()
        user_model.verified = True
        self.session.commit()
        return map_user_model_to_entity(user_model)

    def find_by_email(self, email: str) -> User | None:
        """Trouver un utilisateur par son email"""
        user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
        if user_model is None:
            return None
        return map_user_model_to_entity(user_model)
