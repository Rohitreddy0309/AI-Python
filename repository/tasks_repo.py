"""Repository for task database operations."""

from sqlalchemy.orm import Session

from models.tasks import Task


class TaskRepository:
    """CRUD operations for the Task model."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_tasks(self):
        """Return all task records."""
        return self.db.query(Task).all()

    def create_task(self, task):
        """Persist a new task record."""
        new_task = Task(
            title=task.title, description=task.description, completed=task.completed
        )

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return new_task

    def update_task(self, task_id, task_data):
        """Update an existing task record."""

        task = self.db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return None

        task.title = task_data.title
        task.description = task_data.description
        task.completed = task_data.completed

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete_task(self, task_id):
        """Delete a task record."""

        task = self.db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return None

        self.db.delete(task)
        self.db.commit()

        return task

    def update_task_file(self, task_id, filename):
        """Attach a file name to an existing task record."""

        task = self.db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return None

        task.file_name = filename
        self.db.commit()
        self.db.refresh(task)

        return task
