"""Dependency providers related to employee use cases."""

from fastapi import Depends
from sqlalchemy.orm import Session

from core.db import get_db
from repository.employees_repo import EmployeeRepository
from service.emp_service import EmployeeService


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Create and return an EmployeeService instance.

    This is used by FastAPI's dependency injection system in route handlers.
    """

    repository = EmployeeRepository(db)
    service = EmployeeService(repository)

    return service
