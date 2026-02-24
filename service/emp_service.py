from sqlalchemy.orm import Session
from repository import employees_repo



def list_all_employees(db: Session):
    return employees_repo.get_all_employees(db)

def get_employee_by_id(db: Session, employee_id: int):
    return employees_repo.get_employee_by_id(db, employee_id)

def create_employee(db: Session, employee_data: dict):
    return employees_repo.create_employee_db(db, employee_data)       

def update_employee(db: Session, employee_id: int, employee_data):
    return employees_repo.update_employee(db, employee_id, employee_data)

def delete_employee(db: Session, employee_id: int):
    return employees_repo.delete_employee(db, employee_id)

def get_employees_by_department(db: Session, department: str):
    return employees_repo.get_employees_by_department(db, department)
