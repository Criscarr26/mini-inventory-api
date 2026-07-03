from fastapi import FastAPI
from .routers import products, movements

app = FastAPI(title="Mini Inventory API")

app.include_router(products.router)
app.include_router(movements.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
