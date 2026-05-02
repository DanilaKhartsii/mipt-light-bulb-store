from typing import Optional
from sqlalchemy.orm import Session
from .. import models, schemas


def list_visible_goods(
    db: Session,
    page: int,
    limit: int,
    socle_id: Optional[int] = None,
    shape_id: Optional[int] = None,
    type_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> dict:
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


def get_visible_good(db: Session, good_id: int) -> Optional[models.Good]:
    return db.query(models.Good).filter(
        models.Good.good_id == good_id,
        models.Good.is_visible == True,
    ).first()


def list_all_goods(db: Session, page: int, limit: int) -> dict:
    total = db.query(models.Good).count()
    items = db.query(models.Good).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


def get_good_by_id(db: Session, good_id: int) -> Optional[models.Good]:
    return db.query(models.Good).filter(models.Good.good_id == good_id).first()


def create_good(db: Session, data: schemas.GoodCreate) -> models.Good:
    good = models.Good(**data.model_dump())
    db.add(good)
    db.commit()
    db.refresh(good)
    return good


def update_good(db: Session, good: models.Good, data: schemas.GoodUpdate) -> models.Good:
    for field, value in data.model_dump().items():
        setattr(good, field, value)
    db.commit()
    db.refresh(good)
    return good


def set_visibility(db: Session, good: models.Good, is_visible: bool) -> models.Good:
    good.is_visible = is_visible
    db.commit()
    db.refresh(good)
    return good


def delete_good(db: Session, good: models.Good) -> None:
    db.delete(good)
    db.commit()