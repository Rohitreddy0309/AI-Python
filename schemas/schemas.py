from pydantic import BaseModel, ConfigDict
from datetime import date


class PlantBase(BaseModel):
    name: str
    watering_interval_days: int
    sunlight: str
    last_watered: date


class PlantCreate(PlantBase):
    pass


class PlantUpdate(BaseModel):
    name: str | None = None
    watering_interval_days: int | None = None
    sunlight: str | None = None
    last_watered: date | None = None


class PlantResponse(PlantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
class PlantBulkUpdate(BaseModel):
    id: int
    name: str 
    watering_interval_days: int
    sunlight: str
    last_watered: date
    image_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
             
        