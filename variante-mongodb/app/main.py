from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import products, movements

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(movements.router, prefix="/movements", tags=["movements"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini Inventory API"}