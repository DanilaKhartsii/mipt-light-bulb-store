from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SocleResponse(BaseModel):
    socle_id: int
    title: str
    model_config = {"from_attributes": True}


class SocleCreate(BaseModel):
    title: str


class ShapeResponse(BaseModel):
    shape_id: int
    title: str
    model_config = {"from_attributes": True}


class ShapeCreate(BaseModel):
    title: str


class TypeResponse(BaseModel):
    type_id: int
    title: str
    model_config = {"from_attributes": True}


class TypeCreate(BaseModel):
    title: str


class SupplierResponse(BaseModel):
    supplier_id: int
    name: str
    model_config = {"from_attributes": True}


class SupplierCreate(BaseModel):
    name: str


class SupplierGoodLink(BaseModel):
    good_id: int


class GoodResponse(BaseModel):
    good_id: int
    socle_id: Optional[int] = None
    shape_id: Optional[int] = None
    type_id: Optional[int] = None
    suppliers_id: Optional[int] = None
    title: str
    price: float
    quantity: int
    description: Optional[str] = None
    size: Optional[float] = None
    illumination: Optional[int] = None
    power: Optional[int] = None
    awaited_delivery_time: Optional[datetime] = None
    is_visible: bool
    model_config = {"from_attributes": True}


class GoodCreate(BaseModel):
    socle_id: Optional[int] = None
    shape_id: Optional[int] = None
    type_id: Optional[int] = None
    suppliers_id: Optional[int] = None
    title: str
    price: float
    quantity: int = 0
    description: Optional[str] = None
    size: Optional[float] = None
    illumination: Optional[int] = None
    power: Optional[int] = None
    awaited_delivery_time: Optional[datetime] = None
    is_visible: bool = False


class GoodUpdate(GoodCreate):
    pass


class VisibilityUpdate(BaseModel):
    is_visible: bool


class PaginatedGoods(BaseModel):
    total: int
    page: int
    limit: int
    items: List[GoodResponse]