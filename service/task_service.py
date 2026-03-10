"""Business logic for task operations."""

from repository.tasks_repo import TaskRepository


class TaskService:
    """Service layer handling task CRUD operations."""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_all_tasks(self):
        """Return a list of all tasks."""
        return self.repository.get_all_tasks()

    def create_new_task(self, task):
        """Create a new task."""
        return self.repository.create_task(task)

    def update_task(self, task_id, task_data):
        """Update an existing task by ID."""
        return self.repository.update_task(task_id, task_data)

    def delete_task(self, task_id):
        """Delete a task by ID."""
        return self.repository.delete_task(task_id)

    def attach_file_to_task(self, task_id, filename):
        """Attach a filename to a task record."""
        return self.repository.update_task_file(task_id, filename)
