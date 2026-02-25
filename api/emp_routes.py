from fastapi import  Depends, HTTPException, Request,Body,APIRouter
from sqlalchemy.orm import Session

from core.db import get_db,Base, engine
from schemas.emp_schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from repository.employees_repo import Employee
from service import emp_service

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/employees", tags=["Employees"])

 

@router.get("/")
def read_root():
    return{"message":"CORS is working!"}

@router.get("/employees", response_model=list[EmployeeResponse])
def get_all_employees(employee: EmployeeResponse = Depends(get_db)):
    return emp_service.list_all_employees(employee)

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return emp_service.create_employee(db, employee.dict())



@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    updated = emp_service.update_employee(db, employee_id, employee.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = emp_service.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted successfully"}
