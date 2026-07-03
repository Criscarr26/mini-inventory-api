from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException
from app.models.product import Product
from app.models.movement import Movement

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.database = self.client[db_name]

    async def close(self):
        self.client.close()

    async def create_product(self, product_data: dict) -> Product:
        product = await self.database.products.insert_one(product_data)
        return await self.database.products.find_one({"_id": product.inserted_id})

    async def get_product(self, product_id: str) -> Product:
        product = await self.database.products.find_one({"_id": ObjectId(product_id)})
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def update_product(self, product_id: str, product_data: dict) -> Product:
        await self.database.products.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> dict:
        result = await self.database.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"detail": "Product deleted"}

    async def create_movement(self, movement_data: dict) -> Movement:
        movement = await self.database.movements.insert_one(movement_data)
        return await self.database.movements.find_one({"_id": movement.inserted_id})

    async def get_movements_by_product(self, product_id: str) -> list:
        movements = await self.database.movements.find({"product_id": product_id}).to_list(length=None)
        return movements

    async def get_movements_by_date_range(self, start_date: str, end_date: str) -> list:
        movements = await self.database.movements.find({
            "ts": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)
        return movements

mongodb = MongoDB(uri="mongodb://localhost:27017", db_name="mini_inventory")