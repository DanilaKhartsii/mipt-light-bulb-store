from datetime import datetime, timezone

from sqlalchemy.orm import Session

from . import models


SOCLES = ["E27", "E14", "GU10", "GU5.3", "G9", "G4", "G13", "R7s"]
SHAPES = ["Груша", "Свеча", "Спот", "Капсула", "Трубка", "Рефлектор"]
SUPPLIER_NAME = "Light Bulb Store"

CATALOG = {
    "Светодиодные лампы": [
        ("LED Classic 7W E27", "E27", "Груша", 149.0, 7, 650, 120),
        ("LED Candle 5W E14", "E14", "Свеча", 129.0, 5, 470, 140),
        ("LED Spot 6W GU10", "GU10", "Спот", 179.0, 6, 520, 90),
        ("LED MR16 7W GU5.3", "GU5.3", "Спот", 169.0, 7, 560, 100),
        ("LED Capsule 4W G9", "G9", "Капсула", 159.0, 4, 360, 60),
        ("LED Mini 3W G4", "G4", "Капсула", 139.0, 3, 250, 80),
        ("LED Tube 18W G13", "G13", "Трубка", 349.0, 18, 1800, 45),
        ("LED Linear 12W R7s", "R7s", "Трубка", 319.0, 12, 1180, 50),
    ],
    "Филаментные лампы": [
        ("Filament Globe 8W E27", "E27", "Груша", 229.0, 8, 806, 75),
        ("Filament Candle 4W E14", "E14", "Свеча", 199.0, 4, 420, 90),
        ("Filament Spot 5W GU10", "GU10", "Спот", 249.0, 5, 450, 60),
        ("Filament MR16 5W GU5.3", "GU5.3", "Спот", 239.0, 5, 430, 60),
        ("Filament Capsule 3W G9", "G9", "Капсула", 219.0, 3, 300, 50),
        ("Filament Mini 2W G4", "G4", "Капсула", 189.0, 2, 180, 50),
        ("Filament Tube 10W G13", "G13", "Трубка", 399.0, 10, 950, 35),
        ("Filament Linear 8W R7s", "R7s", "Трубка", 369.0, 8, 760, 35),
    ],
    "Галогенные лампы": [
        ("Halogen Classic 42W E27", "E27", "Груша", 99.0, 42, 630, 150),
        ("Halogen Candle 28W E14", "E14", "Свеча", 89.0, 28, 370, 120),
        ("Halogen Spot 35W GU10", "GU10", "Спот", 119.0, 35, 400, 80),
        ("Halogen MR16 35W GU5.3", "GU5.3", "Спот", 109.0, 35, 390, 80),
        ("Halogen Capsule 25W G9", "G9", "Капсула", 79.0, 25, 260, 70),
        ("Halogen Mini 20W G4", "G4", "Капсула", 69.0, 20, 220, 70),
        ("Halogen Tube 36W G13", "G13", "Трубка", 149.0, 36, 3350, 30),
        ("Halogen Linear 78W R7s", "R7s", "Трубка", 139.0, 78, 1320, 30),
    ],
    "Умные лампы": [
        ("Smart RGB 9W E27", "E27", "Груша", 699.0, 9, 806, 60),
        ("Smart Candle 6W E14", "E14", "Свеча", 649.0, 6, 520, 50),
        ("Smart Spot 5W GU10", "GU10", "Спот", 749.0, 5, 450, 40),
        ("Smart MR16 5W GU5.3", "GU5.3", "Спот", 729.0, 5, 430, 40),
        ("Smart Capsule 4W G9", "G9", "Капсула", 679.0, 4, 350, 35),
        ("Smart Mini 3W G4", "G4", "Капсула", 599.0, 3, 240, 35),
        ("Smart Tube 16W G13", "G13", "Трубка", 1199.0, 16, 1600, 20),
        ("Smart Linear 10W R7s", "R7s", "Трубка", 999.0, 10, 1000, 25),
    ],
}


def seed_catalog(db: Session) -> None:
    socles = {title: _get_or_create(db, models.Socle, title=title) for title in SOCLES}
    shapes = {title: _get_or_create(db, models.Shape, title=title) for title in SHAPES}
    supplier = _get_or_create(db, models.Supplier, name=SUPPLIER_NAME)
    types = {
        title: _get_or_create(db, models.GoodType, title=title)
        for title in CATALOG
    }

    for type_title, goods in CATALOG.items():
        for title, socle_title, shape_title, price, power, illumination, quantity in goods:
            good = db.query(models.Good).filter(models.Good.title == title).first()
            fields = {
                "socle_id": socles[socle_title].socle_id,
                "shape_id": shapes[shape_title].shape_id,
                "type_id": types[type_title].type_id,
                "suppliers_id": supplier.supplier_id,
                "price": price,
                "quantity": quantity,
                "description": f"{type_title}, цоколь {socle_title}, мощность {power} Вт.",
                "illumination": illumination,
                "power": power,
                "awaited_delivery_time": datetime(2026, 5, 20, tzinfo=timezone.utc),
                "is_visible": True,
            }
            if good is None:
                db.add(models.Good(title=title, **fields))
            else:
                for key, value in fields.items():
                    setattr(good, key, value)

    db.commit()


def _get_or_create(db: Session, model, **fields):
    obj = db.query(model).filter_by(**fields).first()
    if obj is not None:
        return obj

    obj = model(**fields)
    db.add(obj)
    db.flush()
    return obj
