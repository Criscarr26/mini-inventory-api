from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from ..models import MovementCreate, MovementOut
from ..repositories.movements import MovementsRepo
from ..repositories.products import ProductsRepo
from ..services.stock import register_movement, StockError
from ..deps import get_movements_repo, get_products_repo

router = APIRouter(prefix="/api/movements", tags=["movements"])

@router.post("", status_code=201)
async def create_movement(
    payload: MovementCreate,
    moves: MovementsRepo = Depends(get_movements_repo),
    products: ProductsRepo = Depends(get_products_repo),
):
    try:
        result = await register_movement(
            products_repo=products,
            movements_repo=moves,
            product_id=str(payload.product_id),
            type=payload.type,
            qty=payload.qty,
            ts=payload.ts,
        )
        return result
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{product_id}", response_model=list[MovementOut])
async def list_movements(
    product_id: str,
    start: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end: Optional[str] = Query(None, description="YYYY-MM-DD"),
    moves: MovementsRepo = Depends(get_movements_repo),
):
    def parse_date(d: Optional[str]) -> Optional[datetime]:
        if not d:
            return None
        return datetime.fromisoformat(d)
    docs = await moves.list_by_product_and_range(
        product_id=product_id,
        start=parse_date(start),
        end=parse_date(end),
    )
    return docs
