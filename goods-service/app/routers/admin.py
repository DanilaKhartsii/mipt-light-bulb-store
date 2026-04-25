from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/admin", tags=["Администрирование"])


# ── Goods ──────────────────────────────────────────────────────────────────

@router.get("/goods", response_model=schemas.PaginatedGoods)
def admin_list_goods(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(models.Good).count()
    items = db.query(models.Good).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


@router.post("/goods", response_model=schemas.GoodResponse, status_code=201)
def admin_create_good(data: schemas.GoodCreate, db: Session = Depends(get_db)):
    good = models.Good(**data.model_dump())
    db.add(good)
    db.commit()
    db.refresh(good)
    return good


@router.put("/goods/{good_id}", response_model=schemas.GoodResponse)
def admin_update_good(good_id: int, data: schemas.GoodUpdate, db: Session = Depends(get_db)):
    good = db.query(models.Good).filter(models.Good.good_id == good_id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    for field, value in data.model_dump().items():
        setattr(good, field, value)
    db.commit()
    db.refresh(good)
    return good


@router.patch("/goods/{good_id}/visibility", response_model=schemas.GoodResponse)
def admin_toggle_visibility(good_id: int, data: schemas.VisibilityUpdate, db: Session = Depends(get_db)):
    good = db.query(models.Good).filter(models.Good.good_id == good_id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    good.is_visible = data.is_visible
    db.commit()
    db.refresh(good)
    return good


@router.delete("/goods/{good_id}", status_code=204)
def admin_delete_good(good_id: int, db: Session = Depends(get_db)):
    good = db.query(models.Good).filter(models.Good.good_id == good_id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(good)
    db.commit()


# ── Socles ─────────────────────────────────────────────────────────────────

@router.get("/socles", response_model=List[schemas.SocleResponse])
def admin_list_socles(db: Session = Depends(get_db)):
    return db.query(models.Socle).all()


@router.post("/socles", response_model=schemas.SocleResponse, status_code=201)
def admin_create_socle(data: schemas.SocleCreate, db: Session = Depends(get_db)):
    obj = models.Socle(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/socles/{socle_id}", response_model=schemas.SocleResponse)
def admin_update_socle(socle_id: int, data: schemas.SocleCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Socle).filter(models.Socle.socle_id == socle_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Цоколь не найден")
    obj.title = data.title
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/socles/{socle_id}", status_code=204)
def admin_delete_socle(socle_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Socle).filter(models.Socle.socle_id == socle_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Цоколь не найден")
    db.delete(obj)
    db.commit()


# ── Shapes ─────────────────────────────────────────────────────────────────

@router.get("/shapes", response_model=List[schemas.ShapeResponse])
def admin_list_shapes(db: Session = Depends(get_db)):
    return db.query(models.Shape).all()


@router.post("/shapes", response_model=schemas.ShapeResponse, status_code=201)
def admin_create_shape(data: schemas.ShapeCreate, db: Session = Depends(get_db)):
    obj = models.Shape(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/shapes/{shape_id}", response_model=schemas.ShapeResponse)
def admin_update_shape(shape_id: int, data: schemas.ShapeCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Shape).filter(models.Shape.shape_id == shape_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    obj.title = data.title
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/shapes/{shape_id}", status_code=204)
def admin_delete_shape(shape_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Shape).filter(models.Shape.shape_id == shape_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    db.delete(obj)
    db.commit()


# ── Types ──────────────────────────────────────────────────────────────────

@router.get("/types", response_model=List[schemas.TypeResponse])
def admin_list_types(db: Session = Depends(get_db)):
    return db.query(models.GoodType).all()


@router.post("/types", response_model=schemas.TypeResponse, status_code=201)
def admin_create_type(data: schemas.TypeCreate, db: Session = Depends(get_db)):
    obj = models.GoodType(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/types/{type_id}", response_model=schemas.TypeResponse)
def admin_update_type(type_id: int, data: schemas.TypeCreate, db: Session = Depends(get_db)):
    obj = db.query(models.GoodType).filter(models.GoodType.type_id == type_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип не найден")
    obj.title = data.title
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/types/{type_id}", status_code=204)
def admin_delete_type(type_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.GoodType).filter(models.GoodType.type_id == type_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип не найден")
    db.delete(obj)
    db.commit()


# ── Suppliers ──────────────────────────────────────────────────────────────

@router.get("/suppliers", response_model=List[schemas.SupplierResponse])
def admin_list_suppliers(db: Session = Depends(get_db)):
    return db.query(models.Supplier).all()


@router.post("/suppliers", response_model=schemas.SupplierResponse, status_code=201)
def admin_create_supplier(data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    obj = models.Supplier(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierResponse)
def admin_update_supplier(supplier_id: int, data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/suppliers/{supplier_id}", status_code=204)
def admin_delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    db.delete(obj)
    db.commit()


@router.post("/suppliers/{supplier_id}/goods", status_code=201)
def admin_link_supplier_good(
    supplier_id: int,
    data: schemas.SupplierGoodLink,
    db: Session = Depends(get_db),
):
    if not db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first():
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    if not db.query(models.Good).filter(models.Good.good_id == data.good_id).first():
        raise HTTPException(status_code=404, detail="Товар не найден")
    existing = db.query(models.SuppliersToGoods).filter_by(
        suppliers_id=supplier_id, good_id=data.good_id
    ).first()
    if not existing:
        db.add(models.SuppliersToGoods(suppliers_id=supplier_id, good_id=data.good_id))
        db.commit()
    return {"message": "Связь создана"}


@router.delete("/suppliers/{supplier_id}/goods/{good_id}", status_code=204)
def admin_unlink_supplier_good(supplier_id: int, good_id: int, db: Session = Depends(get_db)):
    link = db.query(models.SuppliersToGoods).filter_by(
        suppliers_id=supplier_id, good_id=good_id
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    db.delete(link)
    db.commit()