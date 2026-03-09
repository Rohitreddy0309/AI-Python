"""
Application configuration settings.

This module loads environment variables using Pydantic BaseSettings.
It centralizes configuration such as database connection, application
name, debug mode, environment type, and logging level.
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: Database connection string.
        APP_NAME: Name of the application.
        DEBUG: Enables debug mode.
        ENVIRONMENT: Application environment (development/production).
        LOG_LEVEL: Logging level for the application.
    """

    DATABASE_URL: str
    APP_NAME: str = "Product CRUD API"
    DEBUG: bool = True

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = ConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
