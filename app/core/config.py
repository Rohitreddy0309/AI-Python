import os

class Settings:
    DATABASE_URL: str = "postgresql+psycopg2://postgres:123456789@localhost:5432/postgres"

settings = Settings()