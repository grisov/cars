from datetime import datetime
from fastapi.testclient import TestClient
from random import randint
import re
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string

PATH = f"{settings.API_V1_STR}/vehicles/vehicle"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
PLATE_NUMBER_FORMAT = "^[A-Z]{2}\s[0-9]{4}\s[A-Z]{2}$"


def test_vehicle_get_non_existent(
    client: TestClient,
    db: Session
) -> None:
    """Try to get non-existant vehicle from the empty database."""
    for id in [1, 123, 17539]:
        assert crud.vehicle.get(db, id=id) is None, "There is no such record in the database"
        response = client.get(f"{PATH}/{id}/")
        assert response.status_code == 404, "There is no vehicle with the specified ID"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
        assert response.json()["detail"] == f"Vehicle with ID={id} is not found in the database"


def test_vehicle_get_with_incorrect_id(
    client: TestClient
) -> None:
    """Try to use incorrect ID."""
    for id in [0, -123, "hello", "-", "%", "   ", None]:
        response = client.get(f"{PATH}/{id}/")
        assert response.status_code == 422, "Input data validation error"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_get_correct(
    client: TestClient,
    db: Session
) -> None:
    """Get the vehicle with correct ID from the database."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = f"PS {randint(1000, 9999)} EJ"
    vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    response = client.get(f"{PATH}/{vehicle_in_db.id}/")
    assert response.status_code == 200, "The vehicle was successfully obtained"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == make, "Vehicle manufacturer's name"
    assert vehicle["model"] == model, "Vehicle model name"
    assert vehicle["plate_number"] == plate_number, "Vehicle plate number"
    assert re.match(PLATE_NUMBER_FORMAT, vehicle["plate_number"]), "Vehicle plate number format"
    assert vehicle["id"] == vehicle_in_db.id, "vehicle ID in the database"
    assert "driver_id" in vehicle, "Driver ID in the vehicle"
    assert vehicle["created_at"], "Creation date is not empty"
    assert datetime.strptime(vehicle["created_at"], DATETIME_FORMAT), "The creation date corresponds to the specified format"
    assert vehicle["updated_at"], "Update date is not empty"
    assert datetime.strptime(vehicle["updated_at"], DATETIME_FORMAT), "The update date corresponds to the specified format"
