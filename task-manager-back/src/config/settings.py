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
    jwt_secret_key: str = "34567890-o[pokjlbcdsbcdwen8u]"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Email SMTP (Gmail)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""  # ton-email@gmail.com
    smtp_password: str = ""  # Mot de passe d'application Google
    smtp_from_name: str = "Task Manager"

    # Frontend URL
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
