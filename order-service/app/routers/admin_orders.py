from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas
from ..database import get_db
from ..services import admin_order_service

router = APIRouter(prefix="/admin", tags=["Администрирование заказов"])


@router.get("/orders", response_model=schemas.PaginatedOrders)
def admin_list_orders(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return admin_order_service.list_orders(db, page, limit, status)


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def admin_get_order(order_id: int, db: Session = Depends(get_db)):
    order = admin_order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.patch("/orders/{order_id}/status", response_model=schemas.OrderResponse)
def admin_change_status(order_id: int, data: schemas.StatusUpdate, db: Session = Depends(get_db)):
    order = admin_order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return admin_order_service.update_status(db, order, data.status, data.change_reason)