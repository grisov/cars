from random import choice
from app import crud, schemas
from app.db.session import SessionLocal
from app.tests.utils import random_plate_number


def fill(count: int = 100) -> None:
    """Fill the database with random values."""
    db = SessionLocal()
    for i in range(count):
        first_name = choice((
            "Eugeen", "Peter", "Tetiana", "George", "David", "Borys", "Mark",
            "Helen", "Ruslan", "Oleksandr", "Viktoriya", "Svetlana", "Olha", "Yaromir", "Zdenek", "Thomas"
        ))
        last_name = choice((
            "Rybak", "Hix", "Anders", "Pisarenko", "Poznyak", "Nuland", "Tramp", "Baiden",
            "Homa", "Rojers", "Kozak"
        ))
        driver = crud.driver.create(
            db, obj_in=schemas.DriverCreate(first_name=first_name, last_name=last_name)
        )
        make = choice((
            "Stellantis", "SAIC Motor", "BMW", "Honda", "General Motors", "Ford", "Daimler",
            "Toyota", "Alpina", "Apollo", "Artega", "Audi", "Bitter", "Borgward", "Isdera", "Lotec",
            "MAN", "Mercedes-Benz", "Neoplan", "Opel", "Porsche", "Setra", "Volkswagen", "Wiesmann", "Tesla"
        ))
        model = f"Model {i}"
        plate_number = random_plate_number()
        crud.vehicle.create(
            db=db,
            obj_in=schemas.VehicleCreate(make=make, model=model, plate_number=plate_number),
            driver_id=choice((driver.id, None))
        )
    print("Done")
