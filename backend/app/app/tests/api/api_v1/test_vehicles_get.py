from datetime import datetime
from fastapi.testclient import TestClient
import re
from sqlalchemy.orm import Session
from app.core.config import settings
from app.tests.utils import create_vehicles

PATH = f"{settings.API_V1_STR}/vehicles/vehicle/"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
PLATE_NUMBER_FORMAT = "^[A-Z]{2}\s[0-9]{4}\s[A-Z]{2}$"


def test_vehicles_get_all_from_empty_db(
    client: TestClient,
    db: Session
) -> None:
    """Try to get all vehicles from the empty database."""
    response = client.get(PATH)
    assert response.status_code == 404, "There is no vehicles"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no vehicles in the database that meet the specified criteria"


def test_vehicles_get_all(
    client: TestClient,
    db: Session
) -> None:
    """Get all previously created vehicles."""
    without_driver = create_vehicles(db, with_driver=False)
    with_driver = create_vehicles(db, with_driver=True)
    response = client.get(PATH)
    assert response.status_code == 200, "Successful request"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicles = response.json()
    assert len(vehicles) == without_driver + with_driver, "Total number of vehicles"
    # Check data structure of the each vehicle
    for vehicle in vehicles:
        assert vehicle["id"] > 0, "Vehicle ID in the database"
        assert isinstance(vehicle["make"], str), "Vehicle manufacturer's name"
        assert isinstance(vehicle["model"], str), "Vehicle model name"
        assert isinstance(vehicle["plate_number"], str), "The plate number of the vehicle"
        assert re.match(PLATE_NUMBER_FORMAT, vehicle["plate_number"]), "Vehicle plate number format"
        assert isinstance(vehicle["created_at"], str), "Date of registration of the vehicle in the database"
        assert datetime.strptime(vehicle["created_at"], DATETIME_FORMAT), "Date corresponds to specified format"
        assert isinstance(vehicle["updated_at"], str), "Vehicle information update date"
        assert datetime.strptime(vehicle["updated_at"], DATETIME_FORMAT), "Date corresponds to specified format"
        assert "driver_id" in vehicle, "Driver ID"
        assert len(vehicle) == 7, "The number of properties of each vehicle"


def test_vehicles_get_with_driver_only(
    client: TestClient,
    db: Session
) -> None:
    """Get vehicles with driver only."""
    create_vehicles(db, with_driver=False)
    with_driver = create_vehicles(db, with_driver=True)
    response = client.get(f"{PATH}?with_drivers=yes")
    assert response.status_code == 200, "Successful request"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicles = response.json()
    assert len(vehicles) == with_driver, "Number of vehicles with drivers"


def test_vehicles_get_without_driver_only(
    client: TestClient,
    db: Session
) -> None:
    """Get vehicles without driver only."""
    without_driver = create_vehicles(db, with_driver=False)
    create_vehicles(db, with_driver=True)
    response = client.get(f"{PATH}?with_drivers=no")
    assert response.status_code == 200, "Successful request"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicles = response.json()
    assert len(vehicles) == without_driver, "Number of vehicles without drivers"


def test_vehicles_get_with_wrong_parameter_value(
    client: TestClient,
    db: Session
) -> None:
    """Try to get vehicles by passing an input parameter with an incorrect value."""
    for val in ["", "---", "Hello", 123, 3.14, True, False]:
        response = client.get(f"{PATH}?with_drivers={val}")
        assert response.status_code == 422, "Error validating input parameters"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
