from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    name: str
    email: EmailStr


class StudentCreate(StudentBase):
    """Schema for creating a student."""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating a student."""
    id: int 
    name: str | None = None
    is_active: bool | None = None

class StudentResponse(StudentBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)