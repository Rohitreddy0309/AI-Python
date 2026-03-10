"""
Application configuration settings.

This module loads environment variables using Pydantic BaseSettings.
It is used to manage application configuration such as database URL
and file upload directory.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class for application settings.

    Values are loaded from environment variables or the specified
    .env file.
    """

    db_url: str
    UPLOAD_FOLDER: str

    class Config:
        """
        Configuration for loading environment variables.
        """

        env_file = ".env"


settings = Settings()
