from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from ..models import ProductCreate, ProductUpdate, ProductOut
from ..repositories.products import ProductsRepo
from ..deps import get_products_repo

router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=201)
async def create_product(payload: ProductCreate, repo: ProductsRepo = Depends(get_products_repo)):
    # Ensure unique SKU at app-level (DB also has unique index)
    existing = await repo.get_by_sku(payload.sku)
    if existing:
        raise HTTPException(status_code=409, detail="SKU already exists")
    doc = await repo.create(payload.model_dump())
    return doc

@router.get("", response_model=list[ProductOut])
async def list_products(
    sku: Optional[str] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0),
    stock_min: Optional[int] = Query(None, ge=0),
    stock_max: Optional[int] = Query(None, ge=0),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    repo: ProductsRepo = Depends(get_products_repo),
):
    q: Dict[str, Any] = {}
    if sku:
        q["sku"] = sku
    if name:
        q["name"] = {"$regex": name, "$options": "i"}
    if category:
        q["category"] = {"$regex": category, "$options": "i"}
    price: Dict[str, Any] = {}
    if price_min is not None:
        price["$gte"] = price_min
    if price_max is not None:
        price["$lte"] = price_max
    if price:
        q["price"] = price
    stock: Dict[str, Any] = {}
    if stock_min is not None:
        stock["$gte"] = stock_min
    if stock_max is not None:
        stock["$lte"] = stock_max
    if stock:
        q["stock"] = stock
    docs = await repo.list(q, limit=limit, skip=skip)
    return docs

@router.get("/{id}", response_model=ProductOut)
async def get_product(id: str, repo: ProductsRepo = Depends(get_products_repo)):
    doc = await repo.get_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return doc

@router.patch("/{id}", response_model=ProductOut)
async def update_product(id: str, payload: ProductUpdate, repo: ProductsRepo = Depends(get_products_repo)):
    doc = await repo.update_partial(id, payload.model_dump())
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return doc

@router.delete("/{id}", status_code=204)
async def delete_product(id: str, repo: ProductsRepo = Depends(get_products_repo)):
    ok = await repo.delete_if_no_stock(id)
    if not ok:
        raise HTTPException(status_code=400, detail="Cannot delete: stock must be 0 or product not found")
    return None
