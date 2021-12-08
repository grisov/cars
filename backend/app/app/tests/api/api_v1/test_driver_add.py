from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string

PATH = f"{settings.API_V1_STR}/drivers/driver/"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def test_driver_add_correct(
    client: TestClient,
    db: Session
) -> None:
    """Add a driver using the correct parameters and values."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    response = client.post(PATH, json={"first_name": first_name, "last_name": last_name})
    assert response.status_code == 200, "The driver was added successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    driver = response.json()
    assert driver["first_name"] == first_name, "The first name of the added driver in the database"
    assert driver["last_name"] == last_name, "The last name of the added driver in the database"
    assert driver["id"] == 1, "Driver ID in the database"
    assert driver["created_at"], "Creation date is not empty"
    assert datetime.strptime(driver["created_at"], DATETIME_FORMAT), "The creation date corresponds to the specified format"
    assert driver["updated_at"], "Update date is not empty"
    assert datetime.strptime(driver["updated_at"], DATETIME_FORMAT), "The update date corresponds to the specified format"


def test_driver_add_with_first_name_only(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the driver with only first name."""
    first_name = random_lower_string()
    response = client.post(PATH, json={"first_name": first_name})
    assert response.status_code == 422, "Provided an incomplete data about the driver"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_add_with_last_name_only(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the driver with only last name."""
    last_name = random_lower_string()
    response = client.post(PATH, json={"last_name": last_name})
    assert response.status_code == 422, "Provided an incomplete data about the driver"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_add_without_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the driver without parameters."""
    response = client.post(PATH, json={})
    assert response.status_code == 422, "Provided an incomplete data about the driver"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_add_with_empty_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a driver with empty first and last name."""
    first_name = ""
    last_name = ""
    response = client.post(PATH, json={"first_name": first_name, "last_name": last_name})
    assert response.status_code == 422, "Error validating input parameters"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_add_with_one_symbol_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a driver with one symbol first and last name."""
    first_name = random_lower_string()[0]
    last_name = random_lower_string()[0]
    response = client.post(PATH, json={"first_name": first_name, "last_name": last_name})
    assert response.status_code == 422, "Error validating input parameters"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_add_with_two_symbols_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a driver with two symbols first and last name."""
    first_name = random_lower_string()[:2]
    last_name = random_lower_string()[:2]
    response = client.post(PATH, json={"first_name": first_name, "last_name": last_name})
    assert response.status_code == 200, "The driver was added successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    driver = response.json()
    assert driver["first_name"] == first_name, "The first name of the added driver in the database"
    assert driver["last_name"] == last_name, "The last name of the added driver in the database"
    assert driver["id"] == 1, "Driver ID in the database"
