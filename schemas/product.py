from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    file_name: Optional[str] = None
    file_status: Optional[str] = None
    file_result: Optional[str] = None

    class Config:
        from_attributes = True

class ProductBulkUpdate(ProductBase):
    id: int