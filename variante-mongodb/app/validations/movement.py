from pydantic import BaseModel, validator
from typing import Literal
from fastapi import HTTPException
from app.models.movement import Movement
from app.db.mongodb import get_product_by_id

class MovementCreate(BaseModel):
    product_id: str
    type: Literal['in', 'out']
    qty: int

    @validator('qty')
    def validate_qty(cls, v, values):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero.')
        return v

    async def validate_stock(self):
        product = await get_product_by_id(self.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")
        if self.type == 'out' and product.stock < self.qty:
            raise HTTPException(status_code=400, detail="Insufficient stock for outgoing movement.")

class MovementUpdate(BaseModel):
    qty: int

    @validator('qty')
    def validate_qty(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero.')
        return v