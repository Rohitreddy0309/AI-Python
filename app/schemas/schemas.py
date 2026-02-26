from pydantic import BaseModel, ConfigDict
from datetime import date


# Base schema (shared fields)
class PlantBase(BaseModel):
    name: str
    watering_interval_days: int
    sunlight: str
    last_watered: date


# Schema for creating a plant
class PlantCreate(PlantBase):
    pass


# Schema for updating a plant
class PlantUpdate(BaseModel):
    name: str | None = None
    watering_interval_days: int | None = None
    sunlight: str | None = None
    last_watered: date | None = None


# Schema for returning plant data (response model)
class PlantResponse(PlantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)