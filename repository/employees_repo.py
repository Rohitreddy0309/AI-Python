from sqlalchemy.orm import Session
from schemas.emp_schemas import EmployeeCreate, EmployeeUpdate
from models.employees import Employee

# CRUD operations for Employee model

def get_all_employees(db: Session):
    return db.query(Employee).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def create_employee_db(db: Session, employee_data: dict):
    new_employee = Employee(name=employee_data['name'], department=employee_data['department'], project=employee_data['project'], email=employee_data['email'], blood_group=employee_data['blood_group'], PH_number=employee_data['PH_number'])
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def update_employee(db: Session, employee_id: int, employee_data):
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        return None
    for key, value in employee_data.model_dump().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True

def get_employees_by_department(db: Session, department: str):
    return db.query(Employee).filter(Employee.department == department).all()