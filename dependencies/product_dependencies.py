from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.product_service import ProductService

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)
