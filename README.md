# Mini Inventory API (FastAPI + MongoDB)

Implements a minimal inventory system with products and stock movements.

## Features (as requested)
- CRUD de productos (`sku` único).
- Listado con filtros y paginación.
- `DELETE` solo si `stock == 0`.
- Movimientos de entrada/salida que actualizan el `stock` con validaciones.
- Listado de movimientos por producto y rango de fechas.
- Estructura por capas (routers → services → repositories).
- Pruebas con repositorios en memoria para aislar base de datos.

## Endpoints
- `POST /api/products`
- `GET /api/products` (filtros: `sku`, `name`, `category`, `price_min`, `price_max`, `stock_min`, `stock_max`; paginación: `limit`, `skip`).
- `GET /api/products/{id}`
- `PATCH /api/products/{id}`
- `DELETE /api/products/{id}`
- `POST /api/movements` (body: `product_id`, `type: in|out`, `qty`, `ts` opcional ISO)
- `GET /api/movements/{product_id}?start=YYYY-MM-DD&end=YYYY-MM-DD`

> Nota: El PDF decía `GET /api/movements/{id}/{fecha}` para rango de fechas; aquí se implementa con *query params* `start` y `end`, que es más REST y flexible.

## Arranque rápido (local)

1) Crea y activa un entorno virtual (opcional) e instala dependencias:

```bash
pip install -r requirements.txt
```

2) Variables de entorno (opcional): copia `.env.example` a `.env` y ajusta:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=mini_inventory
```

3) Ejecuta el servidor:
```bash
uvicorn app.main:app --reload
```

## Pruebas

Las pruebas usan repositorios en memoria (sin MongoDB).

```bash
pytest -q
```

## Estructura
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

