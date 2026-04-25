from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
from ..database import get_db

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
    q = db.query(models.Good).filter(models.Good.is_visible == True)
    if socle_id is not None:
        q = q.filter(models.Good.socle_id == socle_id)
    if shape_id is not None:
        q = q.filter(models.Good.shape_id == shape_id)
    if type_id is not None:
        q = q.filter(models.Good.type_id == type_id)
    if min_price is not None:
        q = q.filter(models.Good.price >= min_price)
    if max_price is not None:
        q = q.filter(models.Good.price <= max_price)

    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


@router.get("/goods/{good_id}", response_model=schemas.GoodResponse)
def get_good(good_id: int, db: Session = Depends(get_db)):
    good = db.query(models.Good).filter(
        models.Good.good_id == good_id,
        models.Good.is_visible == True,
    ).first()
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return good