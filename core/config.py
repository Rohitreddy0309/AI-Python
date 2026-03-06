from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "dev"
    APP_NAME: str = "Plant API"
    DEBUG: bool = True
    SECRET_KEY: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()