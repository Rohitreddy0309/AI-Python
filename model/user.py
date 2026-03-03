from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    watering_interval_days = Column(Integer, nullable=False)
    sunlight = Column(String, nullable=False)
    last_watered = Column(DateTime(timezone=True), nullable=False)
    image_url = Column(String, nullable=True)
    