from pydantic import BaseModel, validator
from bson import ObjectId
from typing import Optional
from app.schemas.product import ProductCreate, ProductUpdate

class ProductValidation:
    @staticmethod
    @validator('sku')
    def validate_sku(cls, sku: str):
        if not sku or len(sku) < 3:
            raise ValueError('SKU must be at least 3 characters long.')
        return sku

    @staticmethod
    @validator('price')
    def validate_price(cls, price: float):
        if price < 0:
            raise ValueError('Price must be a non-negative value.')
        return price

    @staticmethod
    @validator('stock')
    def validate_stock(cls, stock: int):
        if stock < 0:
            raise ValueError('Stock must be a non-negative value.')
        return stock

    @staticmethod
    def validate_product_create(product: ProductCreate):
        cls.validate_sku(product.sku)
        cls.validate_price(product.price)
        cls.validate_stock(product.stock)

    @staticmethod
    def validate_product_update(product: ProductUpdate):
        if product.sku:
            cls.validate_sku(product.sku)
        if product.price is not None:
            cls.validate_price(product.price)
        if product.stock is not None:
            cls.validate_stock(product.stock)