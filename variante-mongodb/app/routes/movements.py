from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from app.schemas.movement import MovementCreate, MovementResponse
from app.validations.movement import validate_stock
from app.db.mongodb import get_database

router = APIRouter()

@router.post("/", response_model=MovementResponse)
async def register_movement(movement: MovementCreate, db: MongoClient = Depends(get_database)):
    await validate_stock(movement.product_id, movement.qty, db)
    movement_data = movement.dict()
    movement_data["ts"] = movement_data.get("ts", datetime.utcnow())
    result = await db.movements.insert_one(movement_data)
    movement_data["_id"] = str(result.inserted_id)
    return movement_data

@router.get("/{product_id}", response_model=list[MovementResponse])
async def get_movements(product_id: str, start_date: str = None, end_date: str = None, db: MongoClient = Depends(get_database)):
    query = {"product_id": product_id}
    if start_date:
        query["ts"] = {"$gte": start_date}
    if end_date:
        query["ts"]["$lte"] = end_date
    movements = await db.movements.find(query).to_list(length=100)
    return movements