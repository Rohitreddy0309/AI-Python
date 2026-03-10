from pydantic_settings import BaseSettings
 

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Chethan2004@localhost:5432/studentdb"
    UPLOAD_DIR: str = "app/uploads"

    class Config:
        env_file = ".env"


settings = Settings()