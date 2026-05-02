from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas
from ..database import get_db
from ..services import goods_service

router = APIRouter(tags=["Товары"])


@router.get("/goods", response_model=schemas.PaginatedGoods)
def list_goods(
    socle_id: Optional[int] = None,
    shape_id: Optional[int] = None,
    type_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return goods_service.list_visible_goods(
        db, page, limit,
        socle_id=socle_id, shape_id=shape_id, type_id=type_id,
        min_price=min_price, max_price=max_price,
    )


@router.get("/goods/{good_id}", response_model=schemas.GoodResponse)
def get_good(good_id: int, db: Session = Depends(get_db)):
    good = goods_service.get_visible_good(db, good_id)
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return good