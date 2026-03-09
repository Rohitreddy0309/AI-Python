"""
Pydantic schemas for user data.

This module defines request and response models used for
validating and serializing user-related data in the API.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema used for creating a new user."""

    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    """Schema used for updating user information."""

    name: str | None = None
    is_active: bool | None = None


# pylint: disable=too-few-public-methods
class UserResponse(BaseModel):
    """Schema returned in API responses containing user details."""

    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM compatibility."""

        from_attributes = True
