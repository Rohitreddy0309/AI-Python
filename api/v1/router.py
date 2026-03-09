"""
API v1 Router.

This module registers all version 1 API routes.
"""
from fastapi import APIRouter
from api.v1.routes.student import router as student_router
api_router = APIRouter()

api_router.include_router(
    student_router,
    prefix="/students",
    tags=["Students"],
)
