from sqlalchemy.orm import Session
from random import randint
from app import crud, schemas
from app.tests.utils import random_lower_string


def test_drivers_count_empty(
    db: Session
) -> None:
    """Drivers count in the empty database."""
    count = crud.driver.count(db)
    assert count == 0, "No drivers in the empty database"


def test_drivers_count(
    db: Session
) -> None:
    """Get the number of the previously created drivers."""
    number = randint(10, 100)
    for i in range(number):
        first_name = random_lower_string()
        last_name = random_lower_string()
        driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
        driver = crud.driver.create(db, obj_in=driver_in)
    count = crud.driver.count(db)
    assert count == number, "The number of drivers is correct"
