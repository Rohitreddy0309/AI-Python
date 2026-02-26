from fastapi import APIRouter
from .routes.student import router as student_router
api_router = APIRouter()

api_router.include_router(
    student_router,
    prefix="/students",
    tags=["Students"],
)