"""Business logic for employee operations."""

from repository.employees_repo import EmployeeRepository
from schemas.emp_schemas import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    """Service layer handling employee CRUD operations."""

    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def list_all_employees(self):
        """Return a list of all employees."""
        return self.repository.get_all_employees()

    def create_employee(self, employee: EmployeeCreate):
        """Create a new employee.

        Args:
            employee: The validated employee payload.
        """
        return self.repository.create_employee(employee)

    def update_employee(self, emp_id: int, employee: EmployeeUpdate):
        """Update an existing employee by ID."""
        return self.repository.update_employee(emp_id, employee)

    def delete_employee(self, emp_id: int):
        """Delete an employee by ID."""
        return self.repository.delete_employee(emp_id)
