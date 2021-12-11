from datetime import datetime
from random import randint
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string, random_plate_number


def test_vehicle_get_non_existing(
    db: Session
) -> None:
    """Try to get vehicle with non-existing ID from the empty database."""
    vehicle = crud.vehicle.get(db, id=randint(1, 10000))
    assert vehicle is None, "There is no such record in the database"


def test_vehicle_get_with_incorrect_id(
    db: Session
) -> None:
    """Try to get vehicle with incorrect ID."""
    for id in [-118, 0, "Hello", 3.14, ""]:
        vehicle = crud.vehicle.get(db, id=id)
        assert vehicle is None, "There is no such record in the database"


def test_vehicle_get_correct(
    db: Session
) -> None:
    """Get the previously created vehicle."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    created_vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    assert crud.vehicle.count(db) == 1, "There is 1 record in the database"
    assert created_vehicle.id > 0, "The vehicle has ID in the database"
    vehicle = crud.vehicle.get(db, id=created_vehicle.id)
    assert isinstance(vehicle, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle.id == created_vehicle.id, "The vehicle ID"
    assert vehicle.make == created_vehicle.make, "Manufacturer name of the vehicle"
    assert vehicle.model == created_vehicle.model, "The model of the vehicle"
    assert vehicle.plate_number == created_vehicle.plate_number, "The plate number of the vehicle"
    assert vehicle.created_at == created_vehicle.created_at, "Date of the vehicle registration"
    assert vehicle.updated_at == created_vehicle.updated_at, "Vehicle information update date"
