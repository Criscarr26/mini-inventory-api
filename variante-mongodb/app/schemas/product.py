from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    sku: str = Field(..., description="Unique stock keeping unit")
    name: str = Field(..., description="Name of the product")
    category: str = Field(..., description="Category of the product")
    price: float = Field(..., ge=0, description="Price of the product, must be non-negative")
    stock: int = Field(..., gt=0, description="Stock quantity, must be greater than zero")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    sku: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductInDB(ProductBase):
    created_at: datetime
    updated_at: datetime

class Product(ProductInDB):
    pass