"""
Pydantic schemas for plant data.

This module defines request and response models used for
data validation and serialization in the Plant Care API.
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class PlantBase(BaseModel):
    """Base schema containing common plant attributes."""

    name: str
    watering_interval_days: int
    sunlight: str
    last_watered: date


class PlantCreate(PlantBase):
    """Schema used for creating a new plant."""


class PlantUpdate(BaseModel):
    """Schema used for partially updating plant information."""

    name: str | None = None
    watering_interval_days: int | None = None
    sunlight: str | None = None
    last_watered: date | None = None


class PlantResponse(PlantBase):
    """Schema used for returning plant data in API responses."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class PlantBulkUpdate(BaseModel):
    """Schema used for updating multiple plants in bulk."""

    id: int
    name: str
    watering_interval_days: int
    sunlight: str
    last_watered: date
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
