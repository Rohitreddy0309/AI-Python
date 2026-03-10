"""Pydantic models for task requests/responses."""

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """Shared fields between task create/update/response schemas."""

    title: str
    description: str
    completed: bool = False
    file_name: str | None = None


class TaskCreate(TaskBase):
    """Schema used when creating a new task."""


class TaskUpdate(TaskBase):
    """Schema used when updating an existing task."""


class TaskResponse(TaskBase):
    """Schema returned in responses for task records."""

    id: int


model_config = ConfigDict(from_attributes=True)
