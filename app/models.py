from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

def now_ts() -> datetime:
    return datetime.utcnow()

# ---------- Product Schemas ----------

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    category: Optional[str] = None
    price: float = Field(..., ge=0)

class ProductCreate(ProductBase):
    stock: int = Field(default=0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)

class ProductOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    sku: str
    name: str
    category: Optional[str] = None
    price: float
    stock: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})

# ---------- Movement Schemas ----------

MovementType = Literal["in", "out"]

class MovementCreate(BaseModel):
    product_id: PyObjectId
    type: MovementType
    qty: int = Field(..., gt=0)
    ts: Optional[datetime] = None

    @field_validator("ts")
    @classmethod
    def default_ts(cls, v):
        return v or now_ts()

class MovementOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    product_id: PyObjectId
    type: MovementType
    qty: int
    ts: datetime
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})
