from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.mongodb import get_collection

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    collection = get_collection("products")
    existing_product = await collection.find_one({"sku": product.sku})
    if existing_product:
        raise HTTPException(status_code=400, detail="SKU already exists")
    new_product = Product(**product.dict())
    await collection.insert_one(new_product.dict())
    return new_product

@router.get("/", response_model=List[Product])
async def list_products(skip: int = 0, limit: int = 10):
    collection = get_collection("products")
    products = await collection.find().skip(skip).limit(limit).to_list(length=limit)
    return products

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    collection = get_collection("products")
    product = await collection.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: ProductUpdate):
    collection = get_collection("products")
    updated_product = await collection.find_one_and_update(
        {"_id": product_id},
        {"$set": product_update.dict()},
        return_document=True
    )
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    collection = get_collection("products")
    result = await collection.delete_one({"_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}