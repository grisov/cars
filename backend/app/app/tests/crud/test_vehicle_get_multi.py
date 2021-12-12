from random import randint
from sqlalchemy.orm import Session
from app import crud, models
from app.tests.utils import create_vehicles


def test_vehicles_get_multi_from_empty_db(
    db: Session
) -> None:
    """Try to get vehicles from the empty database."""
    vehicles = crud.vehicle.get_multi(db)
    assert isinstance(vehicles, list), "Received the list of records"
    assert len(vehicles) == 0, "There is no vehicles in the empty database"


def test_vehicles_get_multi_all(
    db: Session
) -> None:
    """Get all previously created vehicles from the database."""
    number = create_vehicles(db, with_driver=False)
    limit = 1000
    assert limit > number, "The limit must exceed the number of records in the database"
    vehicles = crud.vehicle.get_multi(db, skip=0, limit=limit)
    assert isinstance(vehicles, list), "Received the list of records"
    assert len(vehicles) == number, "Received the correct number of vehicles"
    for vehicle in vehicles:
        assert isinstance(vehicle, models.Vehicle), "The type corresponds to the declared model"
        assert vehicle.id > 0, "Each vehicle has an ID in the database"


def test_vehicles_get_multi_skip(
    db: Session
) -> None:
    """Get previously created vehicles except a number of the first records."""
    number = create_vehicles(db, with_driver=False)
    limit = 1000
    assert limit > number, "The limit must exceed the number of records in the database"
    skip = randint(3, 19)
    vehicles = crud.vehicle.get_multi(db, skip=skip, limit=limit)
    assert len(vehicles) < number, "The number of the received vehicles is less than the total"
    for vehicle in vehicles:
        assert vehicle.id >= skip, "Missing all IDs of the skipped vehicles"


def test_vehicles_get_multi_limit(
    db: Session
) -> None:
    """Get only a limited number of vehicles from the database."""
    number = create_vehicles(db, with_driver=False)
    limit = randint(3, 19)
    assert limit < number, "Limited number of vehicles"
    vehicles = crud.vehicle.get_multi(db, skip=0, limit=limit)
    assert len(vehicles) < number, "The number of the received vehicles is less than the total"
    assert len(vehicles) == limit, "The number of received vehicles is limited by the certain value"
    for vehicle in vehicles:
        assert vehicle.id <= limit, "There are no identifiers outside the specified value"


def test_vehicles_get_multi_skip_and_limit(
    db: Session
) -> None:
    """Get previously created vehicles except a number of the first records
    and only a limited number of vehicles from the database.
    """
    number = create_vehicles(db, with_driver=False)
    skip = randint(5, 9)
    limit = randint(10, 19)
    assert skip >= 5, "Skip at least the first 5 entries"
    assert limit < number, "Limited number of vehicles"
    assert skip < limit < number, "Correct values"
    vehicles = crud.vehicle.get_multi(db, skip=skip, limit=limit)
    assert len(vehicles) < number, "The number of the received vehicles is less than the total"
    assert len(vehicles) <= limit, "The number of received vehicles is limited by the certain value"
    for vehicle in vehicles:
        assert vehicle.id >= skip, "Missing all IDs of the skipped vehicles"
        assert vehicle.id <= limit + skip, "There are no identifiers outside the specified value"
