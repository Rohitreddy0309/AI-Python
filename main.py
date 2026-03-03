from fastapi import FastAPI
from core.database import engine, Base
from api.v1.router import api_router
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Care API with PostgreSQL")

# Include API router
app.include_router(api_router, prefix="/api/v1")