from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class MovementCreate(BaseModel):
    product_id: str = Field(..., description="The ID of the product being moved")
    type: Literal['in', 'out'] = Field(..., description="Type of movement: 'in' for incoming stock, 'out' for outgoing stock")
    qty: int = Field(..., gt=0, description="Quantity of the product being moved")
    ts: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the movement")

class Movement(MovementCreate):
    id: str = Field(..., description="The unique identifier for the movement record")