"""
Dependency providers for API routes.

This module provides service instances using FastAPI's
dependency injection system.
"""

# Third-party
from fastapi import Depends
from sqlalchemy.orm import Session

# Local imports
from core.database import get_db
from services.student_service import StudentService
from repositories.student_repository import StudentRepository


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    """
    Create and return a StudentService instance.

    FastAPI automatically injects the database session.
    """

    repository = StudentRepository(db)
    service = StudentService(repository)

    return service
