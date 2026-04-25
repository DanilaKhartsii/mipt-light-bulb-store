from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

ORDER_STATUSES = {"new", "processing", "completed", "cancelled"}

VALID_TRANSITIONS: dict[str, set[str]] = {
    "new": {"processing", "cancelled"},
    "processing": {"completed", "cancelled"},
}


class OrderItemRequest(BaseModel):
    good_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str
    comment: Optional[str] = None
    items: List[OrderItemRequest]


class OrderItemResponse(BaseModel):
    item_id: int
    good_id: int
    good_title: str
    good_sku: str
    price: float
    quantity: int
    subtotal: float
    model_config = {"from_attributes": True}


class StatusHistoryResponse(BaseModel):
    history_id: int
    old_status: Optional[str]
    new_status: str
    changed_by: Optional[str]
    change_reason: Optional[str]
    changed_at: datetime
    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    order_id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    comment: Optional[str]
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]
    status_history: List[StatusHistoryResponse]
    model_config = {"from_attributes": True}


class OrderListItem(BaseModel):
    order_id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    status: str
    total_amount: float
    created_at: datetime
    model_config = {"from_attributes": True}


class PaginatedOrders(BaseModel):
    total: int
    page: int
    limit: int
    items: List[OrderListItem]


class StatusUpdate(BaseModel):
    status: str
    change_reason: Optional[str] = None