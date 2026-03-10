"""
Application configuration module.

This module defines application settings using Pydantic's BaseSettings.
Environment variables are automatically loaded from the `.env` file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        DATABASE_URL (str): Database connection string used by SQLAlchemy.
        UPLOAD_DIR (str): Directory where uploaded files will be stored.
    """

    DATABASE_URL: str = "postgresql://postgres:Chethan2004@localhost:5432/studentdb"
    UPLOAD_DIR: str = "app/uploads"

    class Config:
        """
        Pydantic configuration class.

        Specifies the environment file to load configuration variables from.
        """

        env_file = ".env"


settings = Settings()
"""
Global instance of the Settings class used throughout the application
to access configuration values.
"""
