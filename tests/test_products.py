import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_products_repo

class InMemoryProductsRepo:
    def __init__(self):
        self.data = {}
        self._auto = 0

    async def create(self, data):
        self._auto += 1
        _id = str(self._auto).rjust(24, "0")
        doc = {**data, "_id": _id, "created_at": None, "updated_at": None}
        self.data[_id] = doc
        return doc

    async def get_by_sku(self, sku): 
        for v in self.data.values():
            if v["sku"] == sku:
                return v
        return None

    async def list(self, filters, limit=20, skip=0):
        return list(self.data.values())[skip:skip+limit]

    async def get_by_id(self, id):
        return self.data.get(id)

    async def update_partial(self, id, data):
        if id not in self.data:
            return None
        self.data[id].update({k:v for k,v in data.items() if v is not None})
        return self.data[id]

    async def delete_if_no_stock(self, id):
        doc = self.data.get(id)
        if not doc:
            return False
        if doc.get("stock", 0) != 0:
            return False
        del self.data[id]
        return True

@pytest.fixture(autouse=True)
def override_repo():
    repo = InMemoryProductsRepo()
    app.dependency_overrides[get_products_repo] = lambda: repo
    yield
    app.dependency_overrides.clear()

def test_create_and_get_product():
    client = TestClient(app)
    payload = {"sku":"ABC1","name":"Prod","category":"Cat","price":10,"stock":0}
    r = client.post("/api/products", json=payload)
    assert r.status_code == 201
    prod = r.json()
    r2 = client.get(f"/api/products/{prod['_id']}")
    assert r2.status_code == 200

def test_delete_requires_zero_stock():
    client = TestClient(app)
    payload = {"sku":"ABC2","name":"P2","category":"C","price":5,"stock":5}
    r = client.post("/api/products", json=payload)
    pid = r.json()["_id"]
    rdel = client.delete(f"/api/products/{pid}")
    assert rdel.status_code == 400
