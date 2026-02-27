from fastapi import APIRouter
from api.v1.routes.plant import router as plant_router

api_router = APIRouter()

api_router.include_router(
    plant_router,
    prefix="/plants",
    tags=["Plants"]
)