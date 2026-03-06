from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    APP_NAME: str = "Product CRUD API"
    DEBUG: bool = True

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
