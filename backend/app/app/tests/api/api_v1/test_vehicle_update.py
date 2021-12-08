from datetime import datetime
from fastapi.testclient import TestClient
import re
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string, random_plate_number

PATH = f"{settings.API_V1_STR}/vehicles/vehicle"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
PLATE_NUMBER_FORMAT = "^[A-Z]{2}\s[0-9]{4}\s[A-Z]{2}$"


def test_vehicle_update_non_existent(
    client: TestClient,
    db: Session
) -> None:
    """Try to update non-existant vehicle from the empty database."""
    for id in [1, 123, 1795651]:
        assert crud.vehicle.get(db, id=id) is None, "There is no such record in the database"
        vehicle_in = schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
        response = client.patch(f"{PATH}/{id}/", json=vehicle_in.dict())
        assert response.status_code == 404, "There is no vehicle with the specified ID"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
        assert response.json()["detail"] == f"Vehicle with ID={id} is not found in the database"


def test_vehicle_update_with_incorrect_id(
    client: TestClient
) -> None:
    """Try to use incorrect ID."""
    for id in [0, -123, "hello", "-", "%", "   ", None]:
        vehicle_in = schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
        response = client.patch(f"{PATH}/{id}/", json=vehicle_in.dict())
        assert response.status_code == 422, "Input data validation error"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_update_correct(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle with correct ID from the database."""
    vehicle_in1 = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in1)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_in2 = schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_in2.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_in2.make, "Vehicle manufacturer's name"
    assert vehicle["model"] == vehicle_in2.model, "Vehicle model name"
    assert vehicle["plate_number"] == vehicle_in2.plate_number, "Vehicle plate number"
    assert re.match(PLATE_NUMBER_FORMAT, vehicle["plate_number"]), "Vehicle plate number format"
    assert vehicle["id"] == vehicle_in_db.id, "vehicle ID in the database"
    assert "driver_id" in vehicle, "Driver ID in the vehicle"
    assert vehicle["created_at"], "Creation date is not empty"
    assert datetime.strptime(vehicle["created_at"], DATETIME_FORMAT), "The creation date corresponds to the specified format"
    assert vehicle["updated_at"], "Update date is not empty"
    assert datetime.strptime(vehicle["updated_at"], DATETIME_FORMAT), "The update date corresponds to the specified format"


def test_vehicle_update_make_only(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle make field only."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(make=random_lower_string())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_up.make, "Vehicle manufacturer's name"
    assert vehicle["model"] == vehicle_in.model, "Vehicle model name, not changed"
    assert vehicle["plate_number"] == vehicle_in.plate_number, "Vehicle plate number, not changed"


def test_vehicle_update_model_only(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle model field only."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(model=random_lower_string())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_in.make, "Vehicle manufacturer's name, not changed"
    assert vehicle["model"] == vehicle_up.model, "Vehicle model name"
    assert vehicle["plate_number"] == vehicle_in.plate_number, "Vehicle plate number, not changed"


def test_vehicle_update_plate_number_only(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle plate number field only."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(plate_number=random_plate_number())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_in.make, "Vehicle manufacturer's name, not changed"
    assert vehicle["model"] == vehicle_in.model, "Vehicle model name, not changed"
    assert vehicle["plate_number"] == vehicle_up.plate_number, "Vehicle plate number"


def test_vehicle_update_make_and_model(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle make and model fields."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(make=random_lower_string(), model=random_lower_string())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_up.make, "Vehicle manufacturer's name"
    assert vehicle["model"] == vehicle_up.model, "Vehicle model name"
    assert vehicle["plate_number"] == vehicle_in.plate_number, "Vehicle plate number, not changed"


def test_vehicle_update_make_and_plate_number(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle make and plate number fields."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(make=random_lower_string(), plate_number=random_plate_number())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_up.make, "Vehicle manufacturer's name"
    assert vehicle["model"] == vehicle_in.model, "Vehicle model name, not changed"
    assert vehicle["plate_number"] == vehicle_up.plate_number, "Vehicle plate number"


def test_vehicle_update_model_and_plate_number(
    client: TestClient,
    db: Session
) -> None:
    """Update the vehicle model and plate number fields."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate(model=random_lower_string(), plate_number=random_plate_number())
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_in.make, "Vehicle manufacturer's name, not changed"
    assert vehicle["model"] == vehicle_up.model, "Vehicle model name"
    assert vehicle["plate_number"] == vehicle_up.plate_number, "Vehicle plate number"


def test_vehicle_update_with_empty_values(
    client: TestClient,
    db: Session
) -> None:
    """Try to update the vehicle with empty values (these values ​​are ignored)."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    vehicle_up = schemas.VehicleUpdate()
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json=vehicle_up.dict())
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    vehicle = response.json()
    assert vehicle["make"] == vehicle_in.make, "Vehicle manufacturer's name, not changed"
    assert vehicle["model"] == vehicle_in.model, "Vehicle model name, not changed"
    assert vehicle["plate_number"] == vehicle_in.plate_number, "Vehicle plate number, not changed"


def test_vehicle_update_with_empty_strings(
    client: TestClient,
    db: Session
) -> None:
    """Try to update the vehicle with empty strings."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json={"make": "", "model": "", "plate_number": random_plate_number()})
    assert response.status_code == 422, "Input data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_update_with_one_symbol_strings(
    client: TestClient,
    db: Session
) -> None:
    """Try to update the vehicle with one symbol strings."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json={"make": "A", "model": "B", "plate_number": random_plate_number()})
    assert response.status_code == 422, "Input data validation error"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"


def test_vehicle_update_with_more_than_one_symbol_strings(
    client: TestClient,
    db: Session
) -> None:
    """Try to update the vehicle with more than one symbol strings."""
    vehicle_in = schemas.VehicleCreate(make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number())
    vehicle_in_db = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle_in_db.id > 0, "The vehicle was successfully added to the database"
    for length in range(2, 32):
        make = random_lower_string()[:length]
        model = random_lower_string()[:length]
        response = client.patch(f"{PATH}/{vehicle_in_db.id}/", json={"make": make, "model": model, "plate_number": random_plate_number()})
        assert response.status_code == 200, "The vehicle was successfully updated"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        vehicle = response.json()
        assert vehicle["make"] == make, "Vehicle manufacturer's name"
        assert vehicle["model"] == model, "Vehicle model name"
