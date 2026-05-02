from typing import Optional
from sqlalchemy.orm import Session
import httpx
from fastapi import HTTPException
from .. import models, schemas
from ..clients.goods_client import fetch_good


def create_order(db: Session, data: schemas.OrderCreate) -> models.Order:
    if not data.items:
        raise HTTPException(status_code=422, detail="Список товаров не может быть пустым")

    order_items_data = []
    total = 0.0

    for item in data.items:
        try:
            good = fetch_good(item.good_id)
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError):
            raise HTTPException(status_code=503, detail="Сервис товаров недоступен")
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, detail="Ошибка при получении данных товара")

        if good is None:
            raise HTTPException(
                status_code=422,
                detail=f"Товар {item.good_id} не найден или недоступен для заказа",
            )

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


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()