import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string, random_plate_number


def test_vehicle_update_using_schema(
    db: Session
) -> None:
    """Update the vehicle in the database using schema and check all its attributes."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_make = random_lower_string()
    new_model = random_lower_string()
    new_plate_number = random_plate_number()
    new_vehicle_in = schemas.VehicleUpdate(make=make, model=model, plate_number=plate_number)
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in=new_vehicle_in)
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == vehicle.make, "Manufacturer name of the vehicle"
    assert vehicle_up.model == vehicle.model, "The model of the vehicle"
    assert vehicle_up.plate_number == vehicle.plate_number, "The plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_schema_with_wrong_values(
    db: Session
) -> None:
    """Try to update the vehicle in the database using schema with wrong values
    (all schema string fields must be at least two characters long)
    """
    with pytest.raises(ValidationError):
        schemas.VehicleUpdate(make=random_lower_string()[0], model=random_lower_string(), plate_number=random_plate_number())
        schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string()[0], plate_number=random_plate_number())
        schemas.VehicleUpdate(make=random_lower_string()[0], model=random_lower_string()[0], plate_number=random_plate_number())
        for plate_number in ["", "Hello", -278, 123, 3.14, [], {}, None]:
            schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string(), plate_number=plate_number)


def test_vehicle_update_using_dict_make_only(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with make only."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_make = random_lower_string()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"make": new_make})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == new_make, "New manufacturer name of the vehicle"
    assert vehicle_up.model == model, "The model of the vehicle"
    assert vehicle_up.plate_number == plate_number, "The plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_dict_model_only(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with model only."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_model = random_lower_string()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"model": new_model})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == make, "Manufacturer name of the vehicle"
    assert vehicle_up.model == new_model, "The new model of the vehicle"
    assert vehicle_up.plate_number == plate_number, "The plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_dict_plate_number_only(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with plate_number only."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_plate_number = random_plate_number()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"plate_number": new_plate_number})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == make, "Manufacturer name of the vehicle"
    assert vehicle_up.model == model, "The model of the vehicle"
    assert vehicle_up.plate_number == new_plate_number, "The new plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_dict_make_and_plate_number(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with make and plate_number."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_make = random_lower_string()
    new_plate_number = random_plate_number()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"make": new_make, "plate_number": new_plate_number})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == new_make, "New manufacturer name of the vehicle"
    assert vehicle_up.model == model, "The model of the vehicle"
    assert vehicle_up.plate_number == new_plate_number, "The new plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_dict_model_and_plate_number(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with model and plate_number."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_model = random_lower_string()
    new_plate_number = random_plate_number()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"model": new_model, "plate_number": new_plate_number})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == make, "Manufacturer name of the vehicle"
    assert vehicle_up.model == new_model, "The new model of the vehicle"
    assert vehicle_up.plate_number == new_plate_number, "The new plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_using_dict_make_and_model(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with make and model."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    new_make = random_lower_string()
    new_model = random_lower_string()
    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"make": new_make, "model": new_model})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == new_make, "New manufacturer name of the vehicle"
    assert vehicle_up.model == new_model, "The new model of the vehicle"
    assert vehicle_up.plate_number == plate_number, "The plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"
    assert vehicle_up.driver_id == vehicle.driver_id, "Driver ID in the vehicle"


def test_vehicle_update_driver_id(
    db: Session
) -> None:
    """Update the vehicle in the database using dict with driver_id."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver = crud.driver.create(db, obj_in=driver_in)
    assert driver.id > 0, "The driver ID in the database"

    make = random_lower_string()
    model = random_lower_string()
    plate_number = random_plate_number()
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle.driver is None, "There is no driver in the vehicle"

    vehicle_up = crud.vehicle.update(db, db_obj=vehicle, obj_in={"driver_id": 1})
    assert isinstance(vehicle_up, models.Vehicle), "The created object corresponds to the declared model"
    assert vehicle_up.id == vehicle.id, "The vehicle ID in the database"
    assert vehicle_up.make == make, "Manufacturer name of the vehicle"
    assert vehicle_up.model == model, "The model of the vehicle"
    assert vehicle_up.plate_number == plate_number, "The plate number of the vehicle"
    assert vehicle_up.created_at == vehicle.created_at, "The date of the vehicle registration"
    assert vehicle_up.updated_at <= vehicle.updated_at, "Vehicle information update date"

    assert vehicle_up.driver_id == driver.id, "Driver ID in the vehicle"
    assert isinstance(vehicle_up.driver, models.Driver), "The driver in the vehicle"
    assert vehicle_up.driver.first_name == first_name, "The first name of the driver"
    assert vehicle_up.driver.last_name == last_name, "The last name of the driver"
