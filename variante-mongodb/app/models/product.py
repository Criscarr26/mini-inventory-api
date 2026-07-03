from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit, must be unique")
    name: str = Field(..., description="Name of the product")
    category: str = Field(..., description="Category of the product")
    price: float = Field(..., ge=0, description="Price of the product, must be non-negative")
    stock: int = Field(..., ge=0, description="Available stock, must be greater than or equal to zero")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the product was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the product was last updated")