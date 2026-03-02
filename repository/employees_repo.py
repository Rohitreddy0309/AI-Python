from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models import employees
from schemas.emp_schemas import EmployeeCreate, EmployeeUpdate
from models.employees import Employee
from core.config import logger
from utils.exceptions import NotFoundException, DuplicateEntryException, DatabaseException


# CRUD operations for Employee model

def get_all_employees(db: Session):
    logger.debug("Fetching all employees from the database")
    try:
        employees = db.query(Employee).all()
        logger.info(f"Retrieved {len(employees)} employees from DB")
        return employees
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        return DatabaseException("Error fetching employees from the database")


def get_employee_by_id(db: Session, employee_id: int):
    logger.debug(f"Fetching employee with ID: {employee_id}")
    try:
        employees = db.query(Employee).filter(Employee.id == employee_id).first()
        if employees:
            logger.info(f"Employee found: {employees.name}")
        else:
            logger.warning(f"No employee found with ID: {employee_id}")
        return employees
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise DatabaseException("Error fetching employee from the database")
    

def create_employee_db(db: Session, employee_data: dict):
    logger.debug(f"Creating new employee with data: {employee_data}")
    try:
        new_employee = Employee(name=employee_data['name'], department=employee_data['department'], project=employee_data['project'], email=employee_data['email'], blood_group=employee_data['blood_group'], PH_number=employee_data['PH_number'])
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        logger.info(f"Employee created successfully: {new_employee.name}")
        return new_employee
    except SQLAlchemyError as e:
        logger.error(f"Error creating employee: {e}")
        db.rollback()
        raise DatabaseException("Error creating employee in the database")

def update_employee(db: Session, employee_id: int, employee_data):
    logger.debug(f"Updating employee with ID: {employee_id} using data: {employee_data}")
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        logger.warning(f"Employee with ID: {employee_id} not found for update")
        return None
    try:
        for key, value in employee_data.items():
            setattr(db_employee, key, value)
    
        db.commit()
        db.refresh(db_employee)
        logger.info(f"Employee with ID: {employee_id} updated successfully")
        return db_employee
    except SQLAlchemyError as e:
        logger.error(f"Error updating employeeID : {employee_id}:{e}")
        db.rollback()
        raise DatabaseException("Error updating employee in the database")

def delete_employee(db: Session, employee_id: int):
    logger.debug(f"Attempting to delete employee with ID: {employee_id}")
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        logger.critical(f"Employee with ID: {employee_id} not found for deletion")
        return False
    try:


        db.delete(db_employee)
        db.commit()
        logger.info(f"Employee with ID: {employee_id} deleted successfully")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting employee with ID: {employee_id}: {e}")
        db.rollback()
        raise DatabaseException("Error deleting employee from the database")
