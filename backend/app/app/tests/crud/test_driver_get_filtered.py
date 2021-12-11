from datetime import datetime, timedelta
from random import randint
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests.utils import create_drivers


def test_drivers_get_filtered_from_empty_db(
    db: Session
) -> None:
    """Try to get drivers from the empty database."""
    drivers = crud.driver.get_filtered(db, gte=None, lte=None)
    assert isinstance(drivers, list), "Received the list of records"
    assert len(drivers) == 0, "There is no drivers in the empty database"


def test_drivers_get_filtered_all(
    db: Session
) -> None:
    """Get all previously created drivers from the database."""
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=None, lte=None)
    assert isinstance(drivers, list), "Received the list of records"
    assert len(drivers) == number, "Received the correct number of drivers"
    for driver in drivers:
        assert isinstance(driver, models.Driver), "The type corresponds to the declared model"
        assert driver.id > 0, "Each driver has an ID in the database"


def test_drivers_get_filtered_gte_yesterday(
    db: Session
) -> None:
    """Get drivers created after yesterday."""
    gte = datetime.now() - timedelta(days=2)
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=gte, lte=None)
    assert len(drivers) == number, "All drivers are registered later than yesterday"
    for driver in drivers:
        assert driver.created_at > gte, "Registration date is earlier than yesterday"


def test_drivers_get_filtered_gte_today(
    db: Session
) -> None:
    """Get drivers created after today."""
    gte = datetime.now()
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=gte, lte=None)
    assert len(drivers) == number, "All drivers are registered today"
    for driver in drivers:
        assert driver.created_at >= gte, "Registration date today"


def test_drivers_get_filtered_gte_tomorrow(
    db: Session
) -> None:
    """Get drivers created after tomorrow."""
    gte = datetime.now() + timedelta(days=1)
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=gte, lte=None)
    assert len(drivers) == 0, "There is no drivers registered after tomorrow"


def test_drivers_get_filtered_lte_yesterday(
    db: Session
) -> None:
    """Get drivers created before yesterday."""
    lte = datetime.now() - timedelta(days=1)
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=None, lte=lte)
    assert len(drivers) == 0, "There is no drivers registered before yesterday"


def test_drivers_get_filtered_lte_today(
    db: Session
) -> None:
    """Get drivers created before today."""
    lte = datetime.now()
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=None, lte=lte)
    assert len(drivers) == 0, "There is no drivers registered before today"


def test_drivers_get_filtered_lte_tomorrow(
    db: Session
) -> None:
    """Get drivers created before tomorrow."""
    lte = datetime.now() + timedelta(days=1)
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=None, lte=lte)
    assert len(drivers) == number, "All drivers are registered before tomorrow"
    for driver in drivers:
        assert driver.created_at < lte, "Registration date before tomorrow"


def test_drivers_get_filtered_gte_and_lte(
    db: Session
) -> None:
    """Get drivers created between today and tomorrow."""
    gte = datetime.now()
    lte = datetime.now() + timedelta(days=1)
    number = create_drivers(db)
    drivers = crud.driver.get_filtered(db, gte=gte, lte=lte)
    assert len(drivers) == number, "All drivers are registered today"
    for driver in drivers:
        assert driver.created_at >= gte, "Registration date today"
        assert driver.created_at < lte, "Registration date before tomorrow"
