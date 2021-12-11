import pytest
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string


def test_driver_create_correct(
    db: Session
) -> None:
    """Create the driver in the database and check all its attributes."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver = crud.driver.create(db, obj_in=driver_in)
    assert isinstance(driver, models.Driver), "The created object corresponds to the declared model"
    assert driver.id > 0, "The driver ID"
    assert isinstance(driver.first_name, str), "The first name of the driver"
    assert isinstance(driver.last_name, str), "The last name of the driver"
    assert isinstance(driver.created_at, datetime), "Date of the driver registration"
    assert isinstance(driver.updated_at, datetime), "Driver information update date"


def test_driver_create_with_wrong_values(
    db: Session
) -> None:
    """Try to create the driver in the database using schema with wrong values
    (all schema string fields must be at least two characters long)
    """
    with pytest.raises(ValidationError):
        schemas.DriverCreate(first_name=random_lower_string()[0], last_name=random_lower_string())
        schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string()[0])
        schemas.DriverCreate(first_name=random_lower_string()[0], last_name=random_lower_string()[0])
