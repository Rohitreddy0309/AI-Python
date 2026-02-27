from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.product import ProductCreate, ProductResponse
from services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


# -------------------- READ ALL --------------------
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = ProductService.get_all_products(db)
    return products


# -------------------- READ BY ID --------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# -------------------- CREATE --------------------
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = ProductService.create_product(
        db,
        product.model_dump()
    )
    return new_product


# -------------------- UPDATE --------------------
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    updated_product = ProductService.update_product(
        db,
        product_id,
        product.model_dump()
    )

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


# -------------------- DELETE --------------------
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted = ProductService.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Deleted successfully"}