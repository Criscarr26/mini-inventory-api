from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core import core_schema
from bson import ObjectId

class PyObjectId(ObjectId):
    """ObjectId de MongoDB usable como tipo de Pydantic v2.

    El resto del proyecto ya usa la API v2 (field_validator, ConfigDict), pero
    este tipo se habia quedado en la de v1 (`__get_validators__`). El puente de
    compatibilidad de v2 llama al validador con (valor, info), asi que
    `validate(cls, v)` recibia un argumento de mas y fallaba con "takes 2
    positional arguments but 3 were given" al serializar cualquier respuesta
    que llevara un id.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                str, return_schema=core_schema.str_schema(), when_used="json"
            ),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("ObjectId no valido")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        return handler(core_schema.str_schema())

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

class MovementResult(BaseModel):
    """Respuesta de POST /api/movements: el movimiento y el producto ya ajustado.

    El endpoint no declaraba `response_model`, asi que FastAPI intentaba
    serializar el dict crudo del servicio y fallaba con 500 en cuanto se topaba
    con el ObjectId ("'ObjectId' object is not iterable"). Declarar la forma
    arregla la serializacion y ademas documenta el endpoint en el OpenAPI.
    """
    movement: MovementOut
    product: ProductOut
