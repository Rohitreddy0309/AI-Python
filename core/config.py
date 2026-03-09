"""
Application configuration module.

Loads environment variables using Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    class Config:  # pylint: disable=too-few-public-methods
        """Configuration for loading environment variables."""
        env_file = ".env"


settings = Settings()
