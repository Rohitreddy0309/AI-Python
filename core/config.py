"""Application configuration and logger initialization."""

import logging
import os
from logging.handlers import RotatingFileHandler

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()


# ---------- Logging Setup ----------

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(settings.LOG_LEVEL)

if not logger.handlers:
    logger.addHandler(handler)
