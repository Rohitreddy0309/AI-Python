from fastapi import FastAPI
from app.core.database import engine
from app.models.models import Base
from app.api.v1.routes.plant import router as plant_router
from app.api.v1.router import api_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Care API with PostgreSQL")

app.include_router(plant_router, prefix="/api/v1/plants", tags=["Plants"])