from random import choice, randint
from app.db.session import SessionLocal
from app import crud, schemas


def fill(count: int = 100) -> None:
    """Fill the database with random values."""
    rand_letter = lambda: chr(randint(ord("A"), ord("Z")))
    db = SessionLocal()
    for i in range(count):
        first_name = choice(("Eugeen", "Peter", "Tetiana", "George", "David", "Borys", "Mark", "Helen", "Ruslan", "Oleksandr", "Viktoriya", "Svetlana", "Olha", "Yaromir", "Zdenek", "Thomas"))
        last_name = choice(("Rybak", "Hix", "Anders", "Pisarenko", "Poznyak", "Nuland", "Tramp", "Baiden", "Homa", "Rojers", "Kozak"))
        driver = crud.driver.create(db, obj_in=schemas.DriverCreate(first_name=first_name, last_name=last_name))
        make = choice(("Stellantis", "SAIC Motor", "BMW", "Honda", "General Motors", "Ford", "Daimler", "Toyota", "Alpina", "Apollo", "Artega", "Audi", "Bitter", "Borgward", "Isdera", "Lotec", "MAN", "Mercedes-Benz", "Neoplan", "Opel", "Porsche", "Setra", "Volkswagen", "Wiesmann", "Tesla"))
        model = f"Model {i}"
        plate_number = rand_letter() + rand_letter() + " " + str(randint(1000, 9999)) + " " + rand_letter() + rand_letter()
        vehicle = crud.vehicle.create(db, obj_in=schemas.VehicleCreate(make=make, model=model, plate_number=plate_number), driver_id=choice((driver.id, None)))
    print("Done")
