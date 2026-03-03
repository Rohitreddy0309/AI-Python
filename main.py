from fastapi import FastAPI
from core.database import engine, Base
from api.v1.router import api_router
from fastapi.staticfiles import StaticFiles

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Care API with PostgreSQL")

# Include API router
app.include_router(api_router, prefix="/api/v1")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")