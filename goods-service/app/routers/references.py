from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..services import reference_service

router = APIRouter(tags=["Справочники"])


@router.get("/socles", response_model=List[schemas.SocleResponse])
def list_socles(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.Socle)


@router.get("/shapes", response_model=List[schemas.ShapeResponse])
def list_shapes(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.Shape)


@router.get("/types", response_model=List[schemas.TypeResponse])
def list_types(db: Session = Depends(get_db)):
    return reference_service.list_all(db, models.GoodType)