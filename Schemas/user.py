"""
Pydantic schemas for user-related data validation and serialization.

These schemas define the structure of user data used for creating,
updating, bulk updating, and returning user information in API responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsersBase(BaseModel):
    """
    Base schema containing common user fields.

    This schema is shared by other user schemas to maintain
    consistency in user data representation.
    """

    name: str
    email: str
    department: str
    is_active: bool = True
    photo: Optional[str] = None


class UsersCreate(UsersBase):
    """
    Schema used for creating a new user.

    Inherits all fields from UsersBase.
    """

    pass


class UsersUpdate(BaseModel):
    """
    Schema used for updating an existing user.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    photo: Optional[str] = None


class UsersBulkUpdate(BaseModel):
    """
    Schema used for bulk updating multiple users.

    Only specific fields are allowed to be updated in bulk.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None


class UserResponse(UsersBase):
    """
    Schema used for returning user data in API responses.

    Includes additional fields such as user ID and
    creation date.
    """

    id: int
    created_date: Optional[datetime] = None
    photo: Optional[str] = None

    class Config:
        """
        Configuration for ORM compatibility.
        """

        from_attributes = True
