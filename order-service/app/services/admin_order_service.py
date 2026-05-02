from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas


def list_orders(
    db: Session, page: int, limit: int, status: Optional[str] = None
) -> dict:
    if status and status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=422, detail=f"Недопустимый статус: {status}")
    q = db.query(models.Order)
    if status:
        q = q.filter(models.Order.status == status)
    total = q.count()
    items = q.order_by(models.Order.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()


def update_status(
    db: Session, order: models.Order, new_status: str, change_reason: Optional[str]
) -> models.Order:
    if new_status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=422, detail=f"Недопустимый статус: {new_status}")

    allowed = schemas.VALID_TRANSITIONS.get(order.status, set())
    if new_status not in allowed:
        raise HTTPException(
            status_code=422,
            detail=f"Переход '{order.status}' → '{new_status}' недопустим",
        )

    old_status = order.status
    order.status = new_status
    db.add(models.OrderStatusHistory(
        order_id=order.order_id,
        old_status=old_status,
        new_status=new_status,
        changed_by="admin",
        change_reason=change_reason,
    ))
    db.commit()
    db.refresh(order)
    return order