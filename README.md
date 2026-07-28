# Mini Inventory API (FastAPI + MongoDB)

Implements a minimal inventory system with products and stock movements.

## Features (as requested)
- Product CRUD (unique `sku`).
- Listing with filters and pagination.
- `DELETE` only if `stock == 0`.
- In/out movements that update `stock` with validations.
- Movement listing by product and date range.
- Layered structure (routers → services → repositories).
- Tests with in-memory repositories to isolate the database.

## Endpoints
- `POST /api/products`
- `GET /api/products` (filters: `sku`, `name`, `category`, `price_min`, `price_max`, `stock_min`, `stock_max`; pagination: `limit`, `skip`).
- `GET /api/products/{id}`
- `PATCH /api/products/{id}`
- `DELETE /api/products/{id}`
- `POST /api/movements` (body: `product_id`, `type: in|out`, `qty`, optional ISO `ts`)
- `GET /api/movements/{product_id}?start=YYYY-MM-DD&end=YYYY-MM-DD`

> Note: The PDF said `GET /api/movements/{id}/{fecha}` for date ranges; here it is
> implemented with `start` and `end` *query params*, which is more RESTful and flexible.

## Quick start (local)

1) Create and activate a virtual environment (optional) and install dependencies:

```bash
pip install -r requirements.txt
```

2) Environment variables (optional): copy `.env.example` to `.env` and adjust:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=mini_inventory
```

3) Run the server:
```bash
uvicorn app.main:app --reload
```

## Tests

The tests use in-memory repositories (no MongoDB).

```bash
pytest -q
```

## Structure
```
mini-inventory/
  app/
    main.py
    deps.py
    db.py
    models.py
    repositories/
      products.py
      movements.py
    routers/
      products.py
      movements.py
    services/
      stock.py
  tests/
    test_products.py
    test_movements.py
```


## MongoDB variant

[`variante-mongodb/`](variante-mongodb/) contains a second implementation of the
same API using **MongoDB (async motor)** instead of SQL: the same product and
movement endpoints, with their own schemas and validations. Useful to compare the
same design over two persistence stacks.
