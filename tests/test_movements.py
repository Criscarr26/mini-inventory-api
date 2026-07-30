from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_products_repo, get_movements_repo

class InMemoryProductsRepo:
    def __init__(self):
        self.data = {}
        self._auto = 0

    async def create(self, data):
        self._auto += 1
        _id = str(self._auto).rjust(24, "0")
        now = datetime.utcnow()
        doc = {
            **data,
            "_id": _id,
            "stock": data.get("stock", 0),
            "created_at": now,
            "updated_at": now,
        }
        self.data[_id] = doc
        return doc

    async def get_by_id(self, id):
        return self.data.get(id)

    async def get_by_sku(self, sku):
        # El router de productos comprueba el SKU duplicado antes de crear;
        # sin este metodo el doble falso rompia todo el flujo de movimientos.
        for v in self.data.values():
            if v["sku"] == sku:
                return v
        return None

    async def adjust_stock(self, product_id, delta):
        p = self.data.get(product_id)
        if not p:
            return None
        p["stock"] = p.get("stock",0) + delta
        return p

class InMemoryMovementsRepo:
    def __init__(self):
        self.moves = []

    async def create(self, data):
        data["_id"] = str(len(self.moves)+1).rjust(24, "0")
        self.moves.append(data)
        return data

    async def list_by_product_and_range(self, product_id, start, end):
        out = [m for m in self.moves if str(m["product_id"]) == product_id]
        return out

@pytest.fixture(autouse=True)
def override_repos():
    products = InMemoryProductsRepo()
    moves = InMemoryMovementsRepo()
    async def _prod(): return products
    async def _mov(): return moves
    app.dependency_overrides[get_products_repo] = _prod
    app.dependency_overrides[get_movements_repo] = _mov
    yield
    app.dependency_overrides.clear()

def test_movement_flow():
    client = TestClient(app)
    # create product (through products router)
    p = {"sku":"SKU-X","name":"X","price":1,"stock":0}
    prod = client.post("/api/products", json=p).json()
    pid = prod["_id"]
    # IN 10
    r_in = client.post("/api/movements", json={"product_id": pid, "type":"in", "qty":10})
    assert r_in.status_code == 201
    # OUT 7
    r_out = client.post("/api/movements", json={"product_id": pid, "type":"out", "qty":7})
    assert r_out.status_code == 201
    # OUT 10 should fail (insufficient)
    r_bad = client.post("/api/movements", json={"product_id": pid, "type":"out", "qty":10})
    assert r_bad.status_code == 400
