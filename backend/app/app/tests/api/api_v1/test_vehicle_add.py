from datetime import datetime
from fastapi.testclient import TestClient
import re
from random import randint
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string

PATH = f"{settings.API_V1_STR}/vehicles/vehicle/"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
PLATE_NUMBER_FORMAT = "^[A-Z]{2}\s[0-9]{4}\s[A-Z]{2}$"


def test_vehicle_add_correct(
    client: TestClient,
    db: Session
) -> None:
    """Add a vehicle using the correct parameters and values."""
    make = random_lower_string()
    model = random_lower_string()
    plate_number = f"AL {randint(1000, 9999)} ZQ"
    response = client.post(PATH, json={"make": make, "model": model, "plate_number": plate_number})
    assert response.status_code == 200, "The vehicle was added successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == make, "Vehicle manufacturer's name"
    assert vehicle["model"] == model, "Vehicle model name"
    assert vehicle["plate_number"] == plate_number, "Vehicle plate number"
    assert re.match(PLATE_NUMBER_FORMAT, vehicle["plate_number"]), "Vehicle plate number format"
    assert vehicle["id"] == 1, "vehicle ID in the database"
    assert "driver_id" in vehicle, "Driver ID in the vehicle"
    assert vehicle["created_at"], "Creation date is not empty"
    assert datetime.strptime(vehicle["created_at"], DATETIME_FORMAT), "The creation date corresponds to the specified format"
    assert vehicle["updated_at"], "Update date is not empty"
    assert datetime.strptime(vehicle["updated_at"], DATETIME_FORMAT), "The update date corresponds to the specified format"


def test_vehicle_add_with_make_only(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with only manufacturer's name."""
    make = random_lower_string()
    response = client.post(PATH, json={"make": make})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_model_only(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with model name only."""
    model = random_lower_string()
    response = client.post(PATH, json={"model": model})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_plate_number_only(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with plate number only."""
    plate_number = f"ZT {randint(1000, 9999)} KY"
    response = client.post(PATH, json={"plate_number": plate_number})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_make_and_model(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with make and model."""
    make = random_lower_string()
    model = random_lower_string()
    response = client.post(PATH, json={"make": make, "model": model})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_make_and_plate_number(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with make and plate_number."""
    make = random_lower_string()
    plate_number = f"UA {randint(1000, 9999)} OE"
    response = client.post(PATH, json={"make": make, "plate_number": plate_number})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_model_and_plate_number(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle with model and plate_number."""
    model = random_lower_string()
    plate_number = f"UA {randint(1000, 9999)} OE"
    response = client.post(PATH, json={"model": model, "plate_number": plate_number})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_without_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add the vehicle without parameters."""
    response = client.post(PATH, json={})
    assert response.status_code == 422, "Provided an incomplete data about the vehicle"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_empty_parameters(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a vehicle with empty parameters."""
    make = ""
    model = ""
    plate_number = ""
    response = client.post(PATH, json={"make": make, "model": model, "plate_number": plate_number})
    assert response.status_code == 422, "Incoming data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_one_symbol_make_and_model(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a vehicle with one symbol make and model."""
    make = random_lower_string()[0]
    model = random_lower_string()[0]
    plate_number = f"BF {randint(1000, 9999)} XI"
    response = client.post(PATH, json={"make": make, "model": model, "plate_number": plate_number})
    assert response.status_code == 422, "Incoming data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_add_with_two_symbols_make_and_model(
    client: TestClient,
    db: Session
) -> None:
    """Add a vehicle with two symbols make and model."""
    make = random_lower_string()[:2]
    model = random_lower_string()[:2]
    plate_number = f"VM {randint(1000, 9999)} QW"
    response = client.post(PATH, json={"make": make, "model": model, "plate_number": plate_number})
    assert response.status_code == 200, "The vehicle was added successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["id"] == 1, "vehicle ID in the database"
    assert vehicle["make"] == make, "Vehicle manufacturer's name"
    assert vehicle["model"] == model, "Vehicle model name"
    assert vehicle["plate_number"] == plate_number, "Vehicle plate number"


def test_vehicle_add_with_wrong_plate_number_format(
    client: TestClient,
    db: Session
) -> None:
    """Try to add a vehicle with wrong plate number format."""
    make = random_lower_string()
    model = random_lower_string()
    for plate_number in [randint(1000, 9999), random_lower_string()[:6], "", None, "ab 1234 cd"]:
        response = client.post(PATH, json={"make": make, "model": model, "plate_number": plate_number})
        assert response.status_code == 422, "Incoming data validation error"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
