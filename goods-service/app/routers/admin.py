from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..services import goods_service, reference_service

router = APIRouter(prefix="/admin", tags=["Администрирование"])


# ── Goods ──────────────────────────────────────────────────────────────────

@router.get("/goods", response_model=schemas.PaginatedGoods)
def admin_list_goods(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return goods_service.list_all_goods(db, page, limit)


@router.post("/goods", response_model=schemas.GoodResponse, status_code=201)
def admin_create_good(data: schemas.GoodCreate, db: Session = Depends(get_db)):
    return goods_service.create_good(db, data)


@router.put("/goods/{good_id}", response_model=schemas.GoodResponse)
def admin_update_good(good_id: int, data: schemas.GoodUpdate, db: Session = Depends(get_db)):
    good = goods_service.get_good_by_id(db, good_id)
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return goods_service.update_good(db, good, data)


@router.patch("/goods/{good_id}/visibility", response_model=schemas.GoodResponse)
def admin_toggle_visibility(good_id: int, data: schemas.VisibilityUpdate, db: Session = Depends(get_db)):
    good = goods_service.get_good_by_id(db, good_id)
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return goods_service.set_visibility(db, good, data.is_visible)


@router.delete("/goods/{good_id}", status_code=204)
def admin_delete_good(good_id: int, db: Session = Depends(get_db)):
    good = goods_service.get_good_by_id(db, good_id)
    if not good:
        raise HTTPException(status_code=404, detail="Товар не найден")
    goods_service.delete_good(db, good)


# ── Socles ─────────────────────────────────────────────────────────────────

@router.get("/socles", response_model=List[schemas.SocleResponse])
def admin_list_socles(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.Socle)


@router.post("/socles", response_model=schemas.SocleResponse, status_code=201)
def admin_create_socle(data: schemas.SocleCreate, db: Session = Depends(get_db)):
    return reference_service.create_obj(db, models.Socle, data)


@router.put("/socles/{socle_id}", response_model=schemas.SocleResponse)
def admin_update_socle(socle_id: int, data: schemas.SocleCreate, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Socle, models.Socle.socle_id, socle_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Цоколь не найден")
    return reference_service.update_obj(db, obj, title=data.title)


@router.delete("/socles/{socle_id}", status_code=204)
def admin_delete_socle(socle_id: int, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Socle, models.Socle.socle_id, socle_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Цоколь не найден")
    reference_service.delete_obj(db, obj)


# ── Shapes ─────────────────────────────────────────────────────────────────

@router.get("/shapes", response_model=List[schemas.ShapeResponse])
def admin_list_shapes(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.Shape)


@router.post("/shapes", response_model=schemas.ShapeResponse, status_code=201)
def admin_create_shape(data: schemas.ShapeCreate, db: Session = Depends(get_db)):
    return reference_service.create_obj(db, models.Shape, data)


@router.put("/shapes/{shape_id}", response_model=schemas.ShapeResponse)
def admin_update_shape(shape_id: int, data: schemas.ShapeCreate, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Shape, models.Shape.shape_id, shape_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    return reference_service.update_obj(db, obj, title=data.title)


@router.delete("/shapes/{shape_id}", status_code=204)
def admin_delete_shape(shape_id: int, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Shape, models.Shape.shape_id, shape_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    reference_service.delete_obj(db, obj)


# ── Types ──────────────────────────────────────────────────────────────────

@router.get("/types", response_model=List[schemas.TypeResponse])
def admin_list_types(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.GoodType)


@router.post("/types", response_model=schemas.TypeResponse, status_code=201)
def admin_create_type(data: schemas.TypeCreate, db: Session = Depends(get_db)):
    return reference_service.create_obj(db, models.GoodType, data)


@router.put("/types/{type_id}", response_model=schemas.TypeResponse)
def admin_update_type(type_id: int, data: schemas.TypeCreate, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.GoodType, models.GoodType.type_id, type_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Тип не найден")
    return reference_service.update_obj(db, obj, title=data.title)


@router.delete("/types/{type_id}", status_code=204)
def admin_delete_type(type_id: int, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.GoodType, models.GoodType.type_id, type_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Тип не найден")
    reference_service.delete_obj(db, obj)


# ── Suppliers ──────────────────────────────────────────────────────────────

@router.get("/suppliers", response_model=List[schemas.SupplierResponse])
def admin_list_suppliers(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.Supplier)


@router.post("/suppliers", response_model=schemas.SupplierResponse, status_code=201)
def admin_create_supplier(data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return reference_service.create_obj(db, models.Supplier, data)


@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierResponse)
def admin_update_supplier(supplier_id: int, data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Supplier, models.Supplier.supplier_id, supplier_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    return reference_service.update_obj(db, obj, name=data.name)


@router.delete("/suppliers/{supplier_id}", status_code=204)
def admin_delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    obj = reference_service.get_by_id(db, models.Supplier, models.Supplier.supplier_id, supplier_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    reference_service.delete_obj(db, obj)


@router.post("/suppliers/{supplier_id}/goods", status_code=201)
def admin_link_supplier_good(
    supplier_id: int,
    data: schemas.SupplierGoodLink,
    db: Session = Depends(get_db),
):
    if not reference_service.get_by_id(db, models.Supplier, models.Supplier.supplier_id, supplier_id):
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    if not goods_service.get_good_by_id(db, data.good_id):
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
    reference_service.delete_obj(db, link)