from sqlalchemy.orm import Session
from app import crud
from app.tests.utils import create_drivers


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
    number = create_drivers(db)
    count = crud.driver.count(db)
    assert count == number, "The number of drivers is correct"
