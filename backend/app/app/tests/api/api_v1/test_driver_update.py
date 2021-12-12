from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string

PATH = f"{settings.API_V1_STR}/drivers/driver"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def test_driver_update_non_existent(
    client: TestClient,
    db: Session
) -> None:
    """Try to update non-existant driver from the empty database."""
    for id in [1, 123, 1795651]:
        assert crud.driver.get(db, id=id) is None, "There is no such record in the database"
        driver_in = schemas.DriverUpdate(first_name=random_lower_string(), last_name=random_lower_string())
        response = client.patch(f"{PATH}/{id}/", json=driver_in.dict())
        assert response.status_code == 404, "There is no driver with the specified ID"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
        assert response.json()["detail"] == f"Driver with ID={id} is not found in the database"


def test_driver_update_with_incorrect_id(
    client: TestClient
) -> None:
    """Try to use incorrect ID."""
    for id in [0, -123, "hello", "-", "%", "   ", None]:
        driver_in = schemas.DriverUpdate(first_name=random_lower_string(), last_name=random_lower_string())
        response = client.patch(f"{PATH}/{id}/", json=driver_in.dict())
        assert response.status_code == 422, "Input data validation error"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_driver_update_correct(
    client: TestClient,
    db: Session
) -> None:
    """Update the driver with correct ID from the database."""
    driver_in1 = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver_in_db = crud.driver.create(db, obj_in=driver_in1)
    assert driver_in_db.id > 0, "The driver was successfully added to the database"
    driver_in2 = schemas.DriverUpdate(first_name=random_lower_string(), last_name=random_lower_string())
    response = client.patch(f"{PATH}/{driver_in_db.id}/", json=driver_in2.dict())
    assert response.status_code == 200, "The driver was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    driver = response.json()
    assert driver["first_name"] == driver_in2.first_name, "The first name of the updated driver"
    assert driver["first_name"] != driver_in1.first_name, "The previous first name of the driver"
    assert driver["last_name"] == driver_in2.last_name, "The last name of the updated driver"
    assert driver["last_name"] != driver_in1.last_name, "The previous last name of the driver"
    assert driver["id"] == driver_in_db.id, "Driver ID in the database"
    assert driver["created_at"], "Creation date is not empty"
    assert datetime.strptime(driver["created_at"], DATETIME_FORMAT), "Date corresponds to the specified format"
    assert driver["updated_at"], "Update date is not empty"
    assert datetime.strptime(driver["updated_at"], DATETIME_FORMAT), "Date corresponds to the specified format"


def test_driver_update_only_first_name(
    client: TestClient,
    db: Session
) -> None:
    """Try to update only first name of the driver."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver_in_db = crud.driver.create(db, obj_in=driver_in)
    assert driver_in_db.id > 0, "The driver was successfully added to the database"
    response = client.patch(f"{PATH}/{driver_in_db.id}/", json={"first_name": random_lower_string()})
    assert response.status_code == 422, "Input data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_update_only_last_name(
    client: TestClient,
    db: Session
) -> None:
    """Try to update only last name of the driver."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver_in_db = crud.driver.create(db, obj_in=driver_in)
    assert driver_in_db.id > 0, "The driver was successfully added to the database"
    response = client.patch(f"{PATH}/{driver_in_db.id}/", json={"last_name": random_lower_string()})
    assert response.status_code == 422, "Input data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_driver_update_empty_query(
    client: TestClient,
    db: Session
) -> None:
    """Try to update the driver sending empty request body."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver_in_db = crud.driver.create(db, obj_in=driver_in)
    assert driver_in_db.id > 0, "The driver was successfully added to the database"
    response = client.patch(f"{PATH}/{driver_in_db.id}/", json={})
    assert response.status_code == 422, "Input data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
