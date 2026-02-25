import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:ranathi%401306@localhost:5432/Plantdatabase"
)