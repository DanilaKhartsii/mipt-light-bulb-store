from typing import TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session

T = TypeVar("T")


def list_all(db: Session, model: Type[T]) -> List[T]:
    return db.query(model).all()


def get_by_id(db: Session, model: Type[T], pk_column, pk_value: int) -> Optional[T]:
    return db.query(model).filter(pk_column == pk_value).first()


def create_obj(db: Session, model: Type[T], data) -> T:
    obj = model(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_obj(db: Session, obj: Any, **fields) -> Any:
    for key, value in fields.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_obj(db: Session, obj: Any) -> None:
    db.delete(obj)
    db.commit()