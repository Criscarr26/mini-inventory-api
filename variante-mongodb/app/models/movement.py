from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

class Movement(BaseModel):
    product_id: ObjectId
    type: str  # 'in' or 'out'
    qty: int
    ts: datetime = datetime.now()

    class Config:
        json_encoders = {
            ObjectId: str
        }