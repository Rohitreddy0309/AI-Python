from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body

from core.database import get_db
from schemas.product import (
    ProductCreate, 
    ProductResponse,
    ProductBulkUpdate
)

from services.product_service import ProductService

from typing import Union, List
from fastapi import Query
import os
import aiofiles
from fastapi import UploadFile, File, BackgroundTasks
from repositories.product_repository import ProductRepository
from utils.rate_limiter import rate_limit


router = APIRouter(prefix="/products", tags=["Products"])



# ------------------- Single/Bulk CREATE  ----------------
@router.post(
    "/",
    summary="Create Products",
    dependencies=[Depends(rate_limit)]
)
def bulk_create_products(
    products: Union[ProductCreate, List[ProductCreate]],
    db: Session = Depends(get_db)
):
    if isinstance(products, list):
        return ProductService.bulk_create_products(db, products)
    return ProductService.create_product(db, products.model_dump())



# -----------------  BULK READ BY ID  -----------------
@router.get("/", summary="Get Products")
def get_products(
    ids: List[int] | None = Query(None),
    db: Session = Depends(get_db)
):
    if ids:
        return ProductService.get_products_by_ids(db, ids)
    return ProductService.get_all_products(db)



# ------------------  BULK UPDATE  ---------------------
@router.put("/", summary="Update Products")
def bulk_update_products(
    products: List[ProductBulkUpdate],
    db: Session = Depends(get_db)
):
    return ProductService.bulk_update_products(db, products)


# ------------------  BULK DELETE  ---------------------
@router.delete("/", summary="Delete Products")
def bulk_delete_products(
    ids: List[int] = Body(...),
    db: Session = Depends(get_db)
):
    return ProductService.bulk_delete_products(db, ids)


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


# -------------------- UPDATE --------------------
@router.put("/{product_id}", summary="Update Product")
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
@router.delete("/{product_id}", summary="Delete Product")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted = ProductService.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Deleted successfully"}


# ------------------- File Upload -------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post(
        "/{product_id}/upload",
        summary="Upload file product",
        dependencies=[Depends(rate_limit)]
        )
async def upload_product_file(
    product_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    #async save
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    product = ProductRepository.update_file_info(
        db,
        product_id,
        file.filename,
        file_path
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    background_tasks.add_task(
        ProductService.process_product_file,
        product_id
    )

    return {"message": "File uploaded and processing started"}





