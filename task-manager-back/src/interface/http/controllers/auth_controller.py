"""
Controller pour l'authentification
"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from core.dto.auth_dto import LoginDTO, RegisterDTO, TokenDTO, RefreshTokenDTO
from core.dto.user_dto import UserResponseDTO
from core.entities.user import User
from core.services.auth_service import AuthService
from infrastructure.database.repository.user_repository import UserRepositoryImpl
from interface.http.mappers.user_mapper import map_user_entity_to_response


class AuthController:
    """Controller pour les opérations d'authentification"""

    def __init__(self, db: Session):
        self.repository = UserRepositoryImpl(db)
        self.auth_service = AuthService()

    def register(self, dto: RegisterDTO) -> UserResponseDTO:
        """
        Inscrire un nouvel utilisateur
        Retourne None si l'email existe déjà
        """
        # Vérifier si l'email existe déjà
        existing_user = self.repository.find_by_email(dto.email)
        if existing_user is not None:
            return None

        # Créer l'utilisateur avec mot de passe hashé
        now = datetime.now()
        user = User(
            id=uuid4(),
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            password=AuthService.hash_password(dto.password),
            verified=False,
            role=dto.role,
            created_at=now,
            updated_at=now,
        )

        saved_user = self.repository.save(user)
        return map_user_entity_to_response(saved_user)

    def login(self, dto: LoginDTO) -> TokenDTO | None:
        """
        Connecter un utilisateur
        Retourne None si les identifiants sont invalides
        """
        # Trouver l'utilisateur par email
        user = self.repository.find_by_email(dto.email)
        if user is None:
            return None

        # Vérifier le mot de passe
        if not AuthService.verify_password(dto.password, user.password):
            return None

        # Créer les tokens
        access_token = AuthService.create_access_token(user)
        refresh_token = AuthService.create_refresh_token(user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh_token(self, dto: RefreshTokenDTO) -> TokenDTO | None:
        """
        Rafraîchir le token d'accès
        Retourne None si le refresh token est invalide
        """
        # Vérifier que c'est bien un refresh token
        if not AuthService.is_refresh_token(dto.refresh_token):
            return None

        # Vérifier si le token est expiré
        if AuthService.is_token_expired(dto.refresh_token):
            return None

        # Récupérer l'utilisateur
        user_id = AuthService.get_user_id_from_token(dto.refresh_token)
        if user_id is None:
            return None

        user = self.repository.find_by_id(user_id)
        if user is None:
            return None

        # Créer de nouveaux tokens
        access_token = AuthService.create_access_token(user)
        refresh_token = AuthService.create_refresh_token(user)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def get_me(self, user: User) -> UserResponseDTO:
        """Récupérer les informations de l'utilisateur courant"""
        return map_user_entity_to_response(user)
