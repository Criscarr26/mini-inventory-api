from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from .db import get_db
from .repositories.products import ProductsRepo
from .repositories.movements import MovementsRepo

async def get_products_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> ProductsRepo:
    return ProductsRepo(db)

async def get_movements_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> MovementsRepo:
    return MovementsRepo(db)
