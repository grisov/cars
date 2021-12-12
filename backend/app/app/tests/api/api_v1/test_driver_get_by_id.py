from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string

PATH = f"{settings.API_V1_STR}/drivers/driver"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def test_driver_get_non_existent(
    client: TestClient,
    db: Session
) -> None:
    """Try to get non-existant driver from the empty database."""
    for id in [1, 123, 17539]:
        assert crud.driver.get(db, id=id) is None, "There is no such record in the database"
        response = client.get(f"{PATH}/{id}/")
        assert response.status_code == 404, "There is no driver with the specified ID"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
        assert response.json()["detail"] == f"Driver with ID={id} is not found in the database"


def test_driver_get_with_incorrect_id(
    client: TestClient
) -> None:
    """Try to use incorrect ID."""
    for id in [0, -123, "hello", "-", "%", "   ", None]:
        response = client.get(f"{PATH}/{id}/")
        assert response.status_code == 422, "Input data validation error"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_driver_get_correct(
    client: TestClient,
    db: Session
) -> None:
    """Get the driver with correct ID from the database."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    driver_in_db = crud.driver.create(db, obj_in=driver_in)
    assert driver_in_db.id > 0, "The driver was successfully added to the database"
    response = client.get(f"{PATH}/{driver_in_db.id}/")
    assert response.status_code == 200, "The driver was successfully obtained"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    driver = response.json()
    assert driver["first_name"] == first_name, "The first name of the driver"
    assert driver["last_name"] == last_name, "The last name of the driver"
    assert driver["id"] == driver_in_db.id, "Driver ID in the database"
    assert driver["created_at"], "Creation date is not empty"
    assert datetime.strptime(driver["created_at"], DATETIME_FORMAT), "Date corresponds to specified format"
    assert driver["updated_at"], "Update date is not empty"
    assert datetime.strptime(driver["updated_at"], DATETIME_FORMAT), "Date corresponds to specified format"
