from random import randint
from sqlalchemy.orm import Session
from app import crud, models
from app.tests.utils import create_drivers


def test_drivers_get_multi_from_empty_db(
    db: Session
) -> None:
    """Try to get drivers from the empty database."""
    drivers = crud.driver.get_multi(db)
    assert isinstance(drivers, list), "Received the list of records"
    assert len(drivers) == 0, "There is no drivers in the empty database"


def test_drivers_get_multi_all(
    db: Session
) -> None:
    """Get all previously created drivers from the database."""
    number = create_drivers(db)
    limit = 1000
    assert limit > number, "The limit must exceed the number of records in the database"
    drivers = crud.driver.get_multi(db, skip=0, limit=limit)
    assert isinstance(drivers, list), "Received the list of records"
    assert len(drivers) == number, "Received the correct number of drivers"
    for driver in drivers:
        assert isinstance(driver, models.Driver), "The type corresponds to the declared model"
        assert driver.id > 0, "Each driver has an ID in the database"


def test_drivers_get_multi_skip(
    db: Session
) -> None:
    """Get previously created drivers except a number of the first records."""
    number = create_drivers(db)
    limit = 1000
    assert limit > number, "The limit must exceed the number of records in the database"
    skip = randint(3, 19)
    drivers = crud.driver.get_multi(db, skip=skip, limit=limit)
    assert len(drivers) < number, "The number of the received drivers is less than the total"
    for driver in drivers:
        assert driver.id >= skip, "Missing all IDs of the skipped drivers"


def test_drivers_get_multi_limit(
    db: Session
) -> None:
    """Get only a limited number of drivers from the database."""
    number = create_drivers(db)
    limit = randint(3, 19)
    assert limit < number, "Limited number of drivers"
    drivers = crud.driver.get_multi(db, skip=0, limit=limit)
    assert len(drivers) < number, "The number of the received drivers is less than the total"
    assert len(drivers) == limit, "The number of received drivers is limited by the certain value"
    for driver in drivers:
        assert driver.id <= limit, "There are no identifiers outside the specified value"


def test_drivers_get_multi_skip_and_limit(
    db: Session
) -> None:
    """Get previously created drivers except a number of the first records
    and only a limited number of drivers from the database.
    """
    number = create_drivers(db)
    skip = randint(5, 9)
    limit = randint(10, 19)
    assert skip >= 5, "Skip at least the first 5 entries"
    assert limit < number, "Limited number of drivers"
    assert skip < limit < number, "Correct values"
    drivers = crud.driver.get_multi(db, skip=skip, limit=limit)
    assert len(drivers) < number, "The number of the received drivers is less than the total"
    assert len(drivers) == limit, "The number of received drivers is limited by the certain value"
    for driver in drivers:
        assert driver.id >= skip, "Missing all IDs of the skipped drivers"
        assert driver.id <= limit + skip, "There are no identifiers outside the specified value"
