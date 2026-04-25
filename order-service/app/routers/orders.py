import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Заказы"])

GOODS_SERVICE_URL = os.getenv("GOODS_SERVICE_URL", "http://localhost:8001")


@router.post("/orders", response_model=schemas.OrderResponse, status_code=201)
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not data.items:
        raise HTTPException(status_code=422, detail="Список товаров не может быть пустым")

    order_items_data = []
    total = 0.0

    for item in data.items:
        try:
            resp = httpx.get(f"{GOODS_SERVICE_URL}/goods/{item.good_id}", timeout=5.0)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Сервис товаров недоступен")

        if resp.status_code == 404:
            raise HTTPException(
                status_code=422,
                detail=f"Товар {item.good_id} не найден или недоступен для заказа",
            )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Ошибка при получении данных товара")

        good = resp.json()
        subtotal = round(good["price"] * item.quantity, 2)
        total += subtotal

        order_items_data.append({
            "good_id": item.good_id,
            "good_title": good["title"],
            "good_sku": f"GOOD-{item.good_id}",
            "price": good["price"],
            "quantity": item.quantity,
            "subtotal": subtotal,
        })

    order = models.Order(
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        customer_email=data.customer_email,
        comment=data.comment,
        status="new",
        total_amount=round(total, 2),
    )
    db.add(order)
    db.flush()

    for item_data in order_items_data:
        db.add(models.OrderItem(order_id=order.order_id, **item_data))

    db.add(models.OrderStatusHistory(
        order_id=order.order_id,
        old_status=None,
        new_status="new",
        changed_by="system",
        change_reason="Заказ создан",
    ))

    db.commit()
    db.refresh(order)
    return order


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order