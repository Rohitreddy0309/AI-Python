"""
Product API routes.

This module defines all endpoints related to product management,
including CRUD operations, bulk operations, and file uploads.
"""

import os
from typing import List, Union

import aiofiles
from fastapi import (APIRouter, BackgroundTasks, Body, Depends, File, Query,
                     UploadFile)

from dependencies.product_dependencies import get_product_service
from schemas.product import ProductBulkUpdate, ProductCreate, ProductResponse
from services.product_service import ProductService
from utils.exceptions import NotFoundException
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", summary="Create Products", dependencies=[Depends(rate_limit)])
def bulk_create_products(
    products: Union[ProductCreate, List[ProductCreate]],
    service: ProductService = Depends(get_product_service),
):
    """
    Create a single product or multiple products.
    """
    if isinstance(products, list):
        return service.bulk_create_products(products)

    return service.create_product(products.model_dump())


@router.get("/", summary="Get Products", response_model=list[ProductResponse])
def get_products(
    ids: List[int] | None = Query(None),
    service: ProductService = Depends(get_product_service),
):
    """
    Retrieve all products or filter by specific product IDs.
    """
    if ids:
        return service.get_products_by_ids(ids)

    return service.get_all_products()


@router.put("/", summary="Update Products")
def bulk_update_products(
    products: List[ProductBulkUpdate],
    service: ProductService = Depends(get_product_service),
):
    """
    Update multiple products.
    """
    return service.bulk_update_products(products)


@router.delete("/", summary="Delete Products")
def bulk_delete_products(
    ids: List[int] = Body(...), service: ProductService = Depends(get_product_service)
):
    """
    Delete multiple products using product IDs.
    """
    return service.bulk_delete_products(ids)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    """
    Retrieve all products or filter by IDs.
    """

    return service.get_product(product_id)


@router.put("/{product_id}", summary="Update Product")
def update_product(
    product_id: int,
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """
    Update an existing product.
    """
    return service.update_product(product_id, product.model_dump())


@router.delete("/{product_id}", summary="Delete Product")
def delete_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    """
    Delete a product by its ID.
    """
    service.delete_product(product_id)

    return {"message": "Deleted successfully"}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/{product_id}/upload",
    summary="Upload file product",
    dependencies=[Depends(rate_limit)],
)
async def upload_product_file(
    product_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    service: ProductService = Depends(get_product_service),
):
    """
    Upload a file for a specific product and process it in the background.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    product = service.update_file_info(product_id, file.filename, file_path)

    if not product:
        raise NotFoundException("Product not found")

    background_tasks.add_task(service.process_product_file, product_id)

    return {"message": "File uploaded and processing started"}
