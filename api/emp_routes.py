from fastapi import  Depends, HTTPException, Request,Body,APIRouter
from sqlalchemy.orm import Session

from core.db import get_db,Base, engine
from schemas.emp_schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from repository import employees_repo
from service import emp_service
from core.config import logger

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/employees", tags=["Employees"])

 

@router.get("/")
def read_root():
    return{"message":"CORS is working!"}

@router.get("/employees", response_model=list[EmployeeResponse])
def get_all_employees(employee: EmployeeResponse = Depends(get_db)):
    logger.info("Received request to fetch all employees")
    employees=emp_service.list_all_employees(employee)
    if not employees:
        logger.warning("No employees found in the database")
        raise HTTPException(status_code=404, detail="No employees found")
    
    logger.info(f"Returning {len(employees)} employees")
    return employees

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    logger.info(f"Received request to create employee with data: {employee}")

    created_employee = emp_service.create_employee(db, employee.dict())
    if not created_employee:
        logger.error("Failed to create employee")
        raise HTTPException(status_code=500, detail="Failed to create employee")
    
    logger.info(f"Employee created successfully: {created_employee.name}")
    return created_employee



@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update employee with ID: {employee_id} and data: {employee}")

    updated = emp_service.update_employee(db, employee_id, employee.dict())
    if not updated:
        logger.warning(f"Employee with ID: {employee_id} not found for update")
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to delete employee with ID: {employee_id}")
    deleted = emp_service.delete_employee(db, employee_id)
    if not deleted:
        logger.warning(f"Employee with ID: {employee_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Employee not found")
    logger.info(f"Employee with ID: {employee_id} deleted successfully")
    return {"detail": "Employee deleted successfully"}
