from sqlalchemy.orm import Session
from app import crud, models
from app.tests.utils import create_vehicles


def test_vehicles_get_filtered_from_empty_db(
    db: Session
) -> None:
    """Try to get vehicles from the empty database."""
    vehicles = crud.vehicle.get_filtered(db, with_driver=None)
    assert isinstance(vehicles, list), "Received the list of records"
    assert len(vehicles) == 0, "There is no vehicles in the empty database"


def test_vehicles_get_filtered_all(
    db: Session
) -> None:
    """Get all previously created vehicles from the database."""
    without_driver = create_vehicles(db, with_driver=False)
    with_driver = create_vehicles(db, with_driver=True)
    vehicles = crud.vehicle.get_filtered(db, with_driver=None)
    assert isinstance(vehicles, list), "Received the list of records"
    assert len(vehicles) == without_driver + with_driver, "Received the correct number of vehicles"
    for vehicle in vehicles:
        assert isinstance(vehicle, models.Vehicle), "The type corresponds to the declared model"


def test_vehicles_get_filtered_without_drivers_only(
    db: Session
) -> None:
    """Get vehicles without drivers from the database."""
    without_driver = create_vehicles(db, with_driver=False)
    create_vehicles(db, with_driver=True)
    vehicles = crud.vehicle.get_filtered(db, with_driver=False)
    assert len(vehicles) == without_driver, "Only vehicles without driver"
    for vehicle in vehicles:
        assert vehicle.driver_id is None, "There is no driver in the vehicle"


def test_vehicles_get_filtered_with_drivers_only(
    db: Session
) -> None:
    """Get vehicles with drivers from the database."""
    create_vehicles(db, with_driver=False)
    with_driver = create_vehicles(db, with_driver=True)
    vehicles = crud.vehicle.get_filtered(db, with_driver=True)
    assert len(vehicles) == with_driver, "Only vehicles with driver"
    for vehicle in vehicles:
        assert vehicle.driver_id > 0, "The driver is present in the vehicle"  # type: ignore
        assert isinstance(vehicle.driver, models.Driver), "Model with driver details"
        assert len(vehicle.driver.first_name) > 2, "The first name of the driver"
        assert len(vehicle.driver.last_name) > 2, "The last name of the driver"
