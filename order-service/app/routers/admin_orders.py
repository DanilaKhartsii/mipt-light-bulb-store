from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/admin", tags=["Администрирование заказов"])


@router.get("/orders", response_model=schemas.PaginatedOrders)
def admin_list_orders(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if status and status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=422, detail=f"Недопустимый статус: {status}")
    q = db.query(models.Order)
    if status:
        q = q.filter(models.Order.status == status)
    total = q.count()
    items = q.order_by(models.Order.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def admin_get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.patch("/orders/{order_id}/status", response_model=schemas.OrderResponse)
def admin_change_status(order_id: int, data: schemas.StatusUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    if data.status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=422, detail=f"Недопустимый статус: {data.status}")

    allowed = schemas.VALID_TRANSITIONS.get(order.status, set())
    if data.status not in allowed:
        raise HTTPException(
            status_code=422,
            detail=f"Переход '{order.status}' → '{data.status}' недопустим",
        )

    old_status = order.status
    order.status = data.status

    db.add(models.OrderStatusHistory(
        order_id=order_id,
        old_status=old_status,
        new_status=data.status,
        changed_by="admin",
        change_reason=data.change_reason,
    ))

    db.commit()
    db.refresh(order)
    return order