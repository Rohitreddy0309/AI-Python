from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UsersBase(BaseModel):
    name: str
    email: str
    department: str
    is_active: bool = True
    photo: Optional[str] = None


class UsersCreate(UsersBase):
    pass


class UsersUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    photo: Optional[str] = None


class UsersBulkUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None


class UserResponse(UsersBase):
    id: int
    created_date: Optional[datetime] = None
    photo: Optional[str] = None

    class Config:
        from_attributes = True