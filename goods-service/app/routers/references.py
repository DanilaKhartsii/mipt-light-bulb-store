from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Справочники"])


@router.get("/socles", response_model=List[schemas.SocleResponse])
def list_socles(db: Session = Depends(get_db)):
    return db.query(models.Socle).all()


@router.get("/shapes", response_model=List[schemas.ShapeResponse])
def list_shapes(db: Session = Depends(get_db)):
    return db.query(models.Shape).all()


@router.get("/types", response_model=List[schemas.TypeResponse])
def list_types(db: Session = Depends(get_db)):
    return db.query(models.GoodType).all()