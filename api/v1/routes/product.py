from fastapi import APIRouter, Depends
from utils.exceptions import NotFoundException
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
from dependencies.product_dependencies import get_product_service


router = APIRouter(prefix="/products", tags=["Products"])



# ------------------- Single/Bulk CREATE  ----------------
@router.post(
    "/",
    summary="Create Products",
    dependencies=[Depends(rate_limit)]
)
def bulk_create_products(
    products: Union[ProductCreate, List[ProductCreate]],
    service: ProductService = Depends(get_product_service)
):
    
    if isinstance(products, list):
        return service.bulk_create_products(products)
    
    return service.create_product(products.model_dump())



# -----------------  BULK READ BY ID  -----------------
@router.get("/", summary="Get Products")
def get_products(
    ids: List[int] | None = Query(None),
    service: ProductService = Depends(get_product_service)
):
    
    if ids:
        return service.get_products_by_ids(ids)
    
    return service.get_all_products()



# ------------------  BULK UPDATE  ---------------------
@router.put("/", summary="Update Products")
def bulk_update_products(
    products: List[ProductBulkUpdate],
    service: ProductService = Depends(get_product_service)
):
    
    return service.bulk_update_products(products)


# ------------------  BULK DELETE  ---------------------
@router.delete("/", summary="Delete Products")
def bulk_delete_products(
    ids: List[int] = Body(...),
    service: ProductService = Depends(get_product_service)
):
    
    return service.bulk_delete_products(ids)


# -------------------- READ ALL --------------------
@router.get("/", response_model=list[ProductResponse])
def get_products(
    service: ProductService = Depends(get_product_service)
):
    
    return service.get_all_products()


# -------------------- READ BY ID --------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    
    return service.get_product(product_id)


# -------------------- UPDATE --------------------
@router.put("/{product_id}", summary="Update Product")
def update_product(
    product_id: int,
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    
    return service.update_product(
        product_id,
        product.model_dump()
    )


# -------------------- DELETE --------------------
@router.delete("/{product_id}", summary="Delete Product")
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    
    service.delete_product(product_id)

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
    service: ProductService = Depends(get_product_service)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    #async save
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    product = service.update_file_info(
        product_id,
        file.filename,
        file_path
    )

    if not product:
        raise NotFoundException("Product not found")

    background_tasks.add_task(
        service.process_product_file,
        product_id
    )

    return {"message": "File uploaded and processing started"}





