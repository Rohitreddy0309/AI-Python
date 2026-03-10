"""Dependency providers related to task use cases."""

from fastapi import Depends
from sqlalchemy.orm import Session

from core.db import get_db
from repository.tasks_repo import TaskRepository
from service.task_service import TaskService


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Create and return a TaskService instance.

    This is used by FastAPI's dependency injection system in route handlers.
    """

    repository = TaskRepository(db)
    service = TaskService(repository)

    return service
