import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string, random_plate_number


def test_vehicle_create_correct(
    db: Session
) -> None:
    """Create the vehicle in the database and check all its attributes."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    assert isinstance(vehicle, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle.id > 0, "The vehicle ID in the database"
    assert isinstance(vehicle.make, str), "Manufacturer name of the vehicle"
    assert isinstance(vehicle.model, str), "The model of the vehicle"
    assert isinstance(vehicle.plate_number, str), "The plate number of the vehicle"
    assert isinstance(vehicle.created_at, datetime), "The date of the vehicle registration"
    assert isinstance(vehicle.updated_at, datetime), "Vehicle information update date"
    assert hasattr(vehicle, "driver_id"), "Driver ID in the vehicle"


def test_vehicle_create_with_wrong_values(
    db: Session
) -> None:
    """Try to create the vehicle in the database using schema with wrong values
    (all schema string fields must be at least two characters long)
    """
    with pytest.raises(ValidationError):
        schemas.VehicleCreate(make=random_lower_string()[0], model=random_lower_string(), plate_number=random_plate_number())
        schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string()[0], plate_number=random_plate_number())
        schemas.VehicleCreate(make=random_lower_string()[0], model=random_lower_string()[0], plate_number=random_plate_number())
        for plate_number in ["", "Hello", -278, 123, 3.14, [], {}, None]:
            schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=plate_number)
