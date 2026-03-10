"""Repository for employee database operations."""

from sqlalchemy.orm import Session

from models.employees import Employee
from schemas.emp_schemas import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    """CRUD operations for the Employee model."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_employees(self):
        """Return all employee records."""
        return self.db.query(Employee).all()

    def get_employee_by_id(self, emp_id: int):
        """Return a single employee by ID."""
        return self.db.query(Employee).filter(Employee.id == emp_id).first()

    def create_employee(self, employee: EmployeeCreate):
        """Persist a new employee record."""
        new_employee = Employee(
            name=employee.name, email=employee.email, department=employee.department
        )

        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)

        return new_employee

    def update_employee(self, emp_id: int, employee: EmployeeUpdate):
        """Update an existing employee record."""

        db_employee = self.get_employee_by_id(emp_id)

        if not db_employee:
            return None

        db_employee.name = employee.name
        db_employee.email = employee.email
        db_employee.department = employee.department

        self.db.commit()
        self.db.refresh(db_employee)

        return db_employee

    def delete_employee(self, emp_id: int):
        """Delete an employee record."""

        db_employee = self.get_employee_by_id(emp_id)

        if not db_employee:
            return None

        self.db.delete(db_employee)
        self.db.commit()

        return db_employee
