"""
Configuration des variables d'environnement
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration des variables d'environnement
    """

    # Application
    app_env: str = "development"

    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # JWT
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
