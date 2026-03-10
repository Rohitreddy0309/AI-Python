"""Employee API routes.

Defines the FastAPI router and route handlers for employee CRUD operations.
Each handler delegates business logic to the 
:class:`~service.emp_service.EmployeeService` via dependency injection.
"""

from fastapi import APIRouter, Depends, HTTPException

from core.config import logger
from dependencies.emp_dependencies import get_employee_service
from schemas.emp_schemas import (EmployeeCreate, EmployeeResponse,
                                 EmployeeUpdate)
from service.emp_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(service: EmployeeService = Depends(get_employee_service)):
    """Return a list of all employees."""

    logger.info("Fetching all employees")

    employees = service.list_all_employees()

    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")

    return employees


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)
):
    """Create a new employee from the request payload."""

    logger.info("Creating employee %s", employee.name)

    created_employee = service.create_employee(employee)

    return created_employee


@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(
    emp_id: int,
    employee: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
):
    """Update an existing employee by ID."""

    updated_employee = service.update_employee(emp_id, employee)

    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return updated_employee


@router.delete("/{emp_id}")
def delete_employee(
    emp_id: int, service: EmployeeService = Depends(get_employee_service)
):
    """Delete an employee by ID."""

    deleted_employee = service.delete_employee(emp_id)

    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully"}
