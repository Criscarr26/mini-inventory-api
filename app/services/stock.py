from __future__ import annotations
from typing import Dict, Any
from datetime import datetime
from bson import ObjectId

class StockError(Exception):
    pass

async def register_movement(products_repo, movements_repo, *, product_id: str, type: str, qty: int, ts: datetime | None = None) -> Dict[str, Any]:
    if qty <= 0:
        raise StockError("qty must be > 0")
    product = await products_repo.get_by_id(product_id)
    if not product:
        raise StockError("product not found")

    delta = qty if type == "in" else -qty
    if type == "out" and product.get("stock", 0) < qty:
        raise StockError("insufficient stock")

    # Adjust stock atomically
    updated = await products_repo.adjust_stock(product_id, delta)
    if not updated:
        raise StockError("failed to update stock")

    move_doc = await movements_repo.create({
        "product_id": ObjectId(product_id),
        "type": type,
        "qty": qty,
        "ts": ts or datetime.utcnow()
    })
    return {"movement": move_doc, "product": updated}
