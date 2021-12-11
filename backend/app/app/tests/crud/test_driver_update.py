import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string


def test_driver_update_using_schema(
    db: Session
) -> None:
    """Update the driver in the database using schema and check all its attributes."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver = crud.driver.create(db, obj_in=driver_in)
    new_first_name = random_lower_string()
    new_last_name = random_lower_string()
    new_driver_in = schemas.DriverUpdate(first_name=new_first_name, last_name=new_last_name)
    driver_up = crud.driver.update(db, db_obj=driver, obj_in=new_driver_in)
    assert isinstance(driver_up, models.Driver), "The updated object corresponds to the declared model"
    assert driver_up.id == driver.id, "The driver ID"
    assert driver_up.first_name == new_first_name, "The first name of the driver"
    assert driver_up.last_name == new_last_name, "The last name of the driver"
    assert driver_up.created_at == driver.created_at, "Date of the driver registration"
    assert driver_up.updated_at <= driver.updated_at, "Driver information update date"


def test_driver_update_by_schema_with_wrong_values(
    db: Session
) -> None:
    """Try to update the driver in the database using schema with wrong values
    (all schema string fields must be at least two characters long)
    """
    with pytest.raises(ValidationError):
        schemas.DriverUpdate(first_name=random_lower_string()[0], last_name=random_lower_string())
        schemas.DriverUpdate(first_name=random_lower_string(), last_name=random_lower_string()[0])
        schemas.DriverUpdate(first_name=random_lower_string()[0], last_name=random_lower_string()[0])


def test_driver_update_using_dict_with_first_name_only(
    db: Session
) -> None:
    """Update the driver in the database using dict with first_name only."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver = crud.driver.create(db, obj_in=driver_in)
    new_first_name = random_lower_string()
    driver_up = crud.driver.update(db, db_obj=driver, obj_in={"first_name": new_first_name})
    assert isinstance(driver_up, models.Driver), "The updated object corresponds to the declared model"
    assert driver_up.id == driver.id, "The driver ID"
    assert driver_up.first_name == new_first_name, "The new first name of the driver"
    assert driver_up.last_name == last_name, "The last name of the driver"
    assert driver_up.created_at == driver.created_at, "Date of the driver registration"
    assert driver_up.updated_at <= driver.updated_at, "Driver information update date"


def test_driver_update_using_dict_with_last_name_only(
    db: Session
) -> None:
    """Update the driver in the database using dict with last_name only."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver = crud.driver.create(db, obj_in=driver_in)
    new_last_name = random_lower_string()
    driver_up = crud.driver.update(db, db_obj=driver, obj_in={"last_name": new_last_name})
    assert isinstance(driver_up, models.Driver), "The updated object corresponds to the declared model"
    assert driver_up.id == driver.id, "The driver ID"
    assert driver_up.first_name == first_name, "The first name of the driver"
    assert driver_up.last_name == new_last_name, "The new last name of the driver"
    assert driver_up.created_at == driver.created_at, "Date of the driver registration"
    assert driver_up.updated_at <= driver.updated_at, "Driver information update date"
