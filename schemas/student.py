"""
Student schemas.

Defines Pydantic models used for validating and returning
student-related API data.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    """Base schema containing common student fields."""

    name: str
    email: EmailStr


class StudentCreate(StudentBase):
    """Schema for creating a student."""


class StudentUpdate(BaseModel):
    """Schema for updating a student."""

    id: int
    name: str | None = None
    is_active: bool | None = None


class StudentResponse(StudentBase):
    """Schema returned when retrieving student data."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
