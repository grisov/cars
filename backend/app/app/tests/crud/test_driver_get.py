from datetime import datetime
from random import randint
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import random_lower_string


def test_driver_get_non_existing(
    db: Session
) -> None:
    """Try to get driver with non-existing ID from the empty database."""
    driver = crud.driver.get(db, id=randint(1, 10000))
    assert driver is None, "There is no such record in the database"


def test_driver_get_with_incorrect_id(
    db: Session
) -> None:
    """Try to get driver with incorrect ID."""
    for id in [-118, 0, "Hello", 3.14, ""]:
        driver = crud.driver.get(db, id=id)
        assert driver is None, "There is no such record in the database"


def test_driver_get_correct(
    db: Session
) -> None:
    """Get the previously created driver."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    created_driver = crud.driver.create(db, obj_in=driver_in)
    assert crud.driver.count(db) == 1, "There is 1 record in the database"
    assert created_driver.id > 0, "The driver has ID in the database"
    driver = crud.driver.get(db, id=created_driver.id)
    assert isinstance(driver, models.Driver), "The created object corresponds to the declared model"
    assert driver.id == created_driver.id, "The driver ID"
    assert driver.first_name== created_driver.first_name, "The first name of the driver"
    assert driver.last_name == created_driver.last_name, "The last name of the driver"
    assert driver.created_at == created_driver.created_at, "Date of the driver registration"
    assert driver.updated_at == created_driver.updated_at, "Driver information update date"
