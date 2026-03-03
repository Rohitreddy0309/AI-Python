from sqlalchemy import Column, Integer, String, Float, Text
from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    file_status = Column(String, default="PENDING")
    file_result = Column(Text, nullable=True)
    
