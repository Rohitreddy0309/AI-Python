"""Pydantic models for employee requests/responses."""

from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeBase(BaseModel):
    """Shared fields between create/update/response schemas."""

    name: str
    department: str
    project: str
    email: EmailStr
    blood_group: str
    PH_number: str


class EmployeeCreate(EmployeeBase):
    """Schema used when creating a new employee."""


class EmployeeUpdate(EmployeeBase):
    """Schema used when updating an existing employee."""


class EmployeeResponse(EmployeeBase):
    """Schema returned in responses for employee records."""

    id: int


model_config = ConfigDict(from_attributes=True)
