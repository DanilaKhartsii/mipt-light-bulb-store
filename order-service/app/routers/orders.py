from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import order_service

router = APIRouter(tags=["Заказы"])


@router.post("/orders", response_model=schemas.OrderResponse, status_code=201)
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, data)


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order