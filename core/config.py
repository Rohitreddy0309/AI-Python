"""
Configuration settings for the Plant API application.

This module defines application settings using Pydantic BaseSettings.
Environment variables can be loaded from the system or a .env file.
"""

from pydantic_settings import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    ENVIRONMENT: str = "dev"
    APP_NAME: str = "Plant API"
    DEBUG: bool = True
    SECRET_KEY: str = "secret"

    class Config:
        """Configuration for loading environment variables from .env file."""

        env_file = ".env"


settings = Settings()
