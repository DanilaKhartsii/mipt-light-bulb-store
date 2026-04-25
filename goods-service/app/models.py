from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Socle(Base):
    __tablename__ = "socle"

    socle_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    goods = relationship("Good", back_populates="socle")


class Shape(Base):
    __tablename__ = "shape"

    shape_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    goods = relationship("Good", back_populates="shape")


class GoodType(Base):
    __tablename__ = "type"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    goods = relationship("Good", back_populates="good_type")


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class SuppliersToGoods(Base):
    __tablename__ = "suppliers_to_goods"

    suppliers_id = Column(Integer, ForeignKey("suppliers.supplier_id", ondelete="CASCADE"), primary_key=True)
    good_id = Column(Integer, ForeignKey("goods.good_id", ondelete="CASCADE"), primary_key=True)


class Good(Base):
    __tablename__ = "goods"

    good_id = Column(Integer, primary_key=True, autoincrement=True)
    socle_id = Column(Integer, ForeignKey("socle.socle_id"), nullable=True)
    shape_id = Column(Integer, ForeignKey("shape.shape_id"), nullable=True)
    type_id = Column(Integer, ForeignKey("type.type_id"), nullable=True)
    suppliers_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=True)
    title = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    description = Column(Text, nullable=True)
    size = Column(Float, nullable=True)
    illumination = Column(Integer, nullable=True)
    power = Column(Integer, nullable=True)
    awaited_delivery_time = Column(DateTime(timezone=True), nullable=True)
    is_visible = Column(Boolean, default=False, nullable=False)

    socle = relationship("Socle", back_populates="goods")
    shape = relationship("Shape", back_populates="goods")
    good_type = relationship("GoodType", back_populates="goods")
    supplier = relationship("Supplier", foreign_keys=[suppliers_id])