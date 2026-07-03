from __future__ import annotations
from typing import Optional, Dict, Any, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class ProductsRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db["products"]

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
        doc = {
            **data,
            "stock": int(data.get("stock", 0)),
            "created_at": now,
            "updated_at": now,
        }
        res = await self._col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return doc

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        return await self._col.find_one({"_id": ObjectId(id)})

    async def get_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        return await self._col.find_one({"sku": sku})

    async def list(self, filters: Dict[str, Any], limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        cursor = self._col.find(filters).skip(skip).limit(limit).sort("created_at", -1)
        return [doc async for doc in cursor]

    async def update_partial(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = {k: v for k,v in data.items() if v is not None}
        if not data:
            await self._col.update_one({"_id": ObjectId(id)}, {"$set": {"updated_at": datetime.utcnow()}})
            return await self.get_by_id(id)
        data["updated_at"] = datetime.utcnow()
        await self._col.update_one({"_id": ObjectId(id)}, {"$set": data})
        return await self.get_by_id(id)

    async def delete_if_no_stock(self, id: str) -> bool:
        doc = await self.get_by_id(id)
        if not doc:
            return False
        if doc.get("stock", 0) != 0:
            return False
        res = await self._col.delete_one({"_id": ObjectId(id)})
        return res.deleted_count == 1

    async def adjust_stock(self, product_id: str, delta: int) -> Optional[Dict[str, Any]]:
        # Uses atomic update and returns the new doc
        res = await self._col.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": delta}, "$set": {"updated_at": datetime.utcnow()}},
            return_document=True  # type: ignore
        )
        return res
