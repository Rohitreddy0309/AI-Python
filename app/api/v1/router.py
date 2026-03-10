from fastapi import APIRouter
from app.api.v1.routes import file
from app.api.v1.routes import student

api_router = APIRouter()

api_router.include_router(
    file.router,
    prefix="/files",
    tags=["Files"]
)
api_router.include_router(student.router)