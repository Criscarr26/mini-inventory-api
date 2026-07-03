from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class MovementsRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db["movements"]

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        doc = {**data}
        res = await self._col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return doc

    async def list_by_product_and_range(self, product_id: str, start: Optional[datetime], end: Optional[datetime]) -> List[Dict[str, Any]]:
        q: Dict[str, Any] = {"product_id": ObjectId(product_id)}
        if start or end:
            rng: Dict[str, Any] = {}
            if start:
                rng["$gte"] = start
            if end:
                rng["$lte"] = end
            q["ts"] = rng
        cursor = self._col.find(q).sort("ts", -1)
        return [doc async for doc in cursor]
