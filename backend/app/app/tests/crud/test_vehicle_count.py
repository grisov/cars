from sqlalchemy.orm import Session
from random import randint
from app import crud, schemas
from app.tests.utils import random_lower_string, random_plate_number


def test_vehicles_count_empty(
    db: Session
) -> None:
    """Vehicles count in the empty database."""
    count = crud.vehicle.count(db)
    assert count == 0, "No vehicles in the empty database"


def test_vehicles_count(
    db: Session
) -> None:
    """Get the number of the previously created vehicles."""
    number = randint(10, 100)
    for i in range(number):
        make = random_lower_string()
        model = random_lower_string()
        plate_number = random_plate_number()
        vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
        crud.vehicle.create(db, obj_in=vehicle_in)
    count = crud.vehicle.count(db)
    assert count == number, "The number of the vehicles is correct"
