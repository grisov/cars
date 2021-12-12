from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string, random_plate_number

PATH = f"{settings.API_V1_STR}/vehicles/set_driver"


def test_vehicle_set_existing_driver(
    client: TestClient,
    db: Session
) -> None:
    """Set existing driver in to the vehicle."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver = crud.driver.create(db, obj_in=driver_in)
    assert driver.id > 0, "The driver has been successfully added to the database"
    vehicle_in = schemas.VehicleCreate(
        make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number()
    )
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    assert vehicle.id > 0, "The vehicle has been successfully added to the database"
    assert vehicle.driver_id is None, "By default, there is no driver in the vehicle"
    response = client.post(f"{PATH}/{vehicle.id}/", json={"driver_id": driver.id})
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert response.json()["driver_id"] == driver.id, "The driver is present in the vehicle"
    assert response.json()["id"] == vehicle.id, "Vehicle that has been updated"
    assert vehicle.driver.id == driver.id, "Driver ID"
    assert vehicle.driver.first_name == driver_in.first_name, "First name of the driver"
    assert vehicle.driver.last_name == driver_in.last_name, "Last name of the driver"


def test_vehicle_set_non_existing_driver(
    client: TestClient,
    db: Session
) -> None:
    """Try to set non-existing driver in to the vehicle."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver = crud.driver.create(db, obj_in=driver_in)
    assert driver.id > 0, "The driver has been successfully added to the database"
    vehicle_in = schemas.VehicleCreate(
        make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number()
    )
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in, driver_id=driver.id)
    assert vehicle.id > 0, "The vehicle has been successfully added to the database"
    assert vehicle.driver_id == driver.id, "The driver is present in the vehicle"
    for driver_id in range(driver.id + 10, 1011, 100):
        assert crud.driver.get(db, id=driver_id) is None, "There is no such record in the database"
        response = client.post(f"{PATH}/{vehicle.id}/", json={"driver_id": driver_id})
        assert response.status_code == 200, "The vehicle was successfully updated"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert response.json()["driver_id"] == driver.id, "The same driver is in the vehicle"


def test_vehicle_unset_driver(
    client: TestClient,
    db: Session
) -> None:
    """Remove the driver from the vehicle."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver = crud.driver.create(db, obj_in=driver_in)
    assert driver.id > 0, "The driver has been successfully added to the database"
    vehicle_in = schemas.VehicleCreate(
        make=random_lower_string(), model=random_lower_string(), plate_number=random_plate_number()
    )
    vehicle = crud.vehicle.create(db, obj_in=vehicle_in, driver_id=driver.id)
    assert vehicle.id > 0, "The vehicle has been successfully added to the database"
    assert vehicle.driver_id == driver.id, "The driver is present in the vehicle"
    response = client.post(f"{PATH}/{vehicle.id}/", json={"driver_id": None})
    assert response.status_code == 200, "The vehicle was successfully updated"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert response.json()["driver_id"] is None, "There is no driver in the vehicle"
    assert response.json()["id"] == vehicle.id, "Vehicle that has been updated"


def test_vehicle_non_exists_set_driver(
    client: TestClient,
    db: Session
) -> None:
    """Try to set driver in to the non-existing vehicle."""
    driver_in = schemas.DriverCreate(first_name=random_lower_string(), last_name=random_lower_string())
    driver = crud.driver.create(db, obj_in=driver_in)
    assert driver.id > 0, "The driver has been successfully added to the database"
    for id in range(10, 1011, 100):
        response = client.post(f"{PATH}/{id}/", json={"driver_id": driver.id})
        assert response.status_code == 404, "There is no vehicle with the specified ID"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"
        assert response.json()["detail"] == f"Vehicle with ID={id} is not found in the database"
