from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.core.config import settings

PATH = f"{settings.API_V1_STR}/drivers/driver/"


def test_get_drivers_from_empty_db_without_filtering(
    client: TestClient,
    db: Session
) -> None:
    """Check getting all drivers from the empty database without filtering."""
    response = client.get(PATH)
    assert response.status_code == 404, "There are no drivers in the database"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no drivers in the database that meet the specified criteria."


def test_get_existing_single_driver_without_filtering(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing single driver from the database without filtering."""
    driver = schemas.DriverCreate(first_name="asd", last_name="dsa")
    crud.driver.create(db, obj_in=driver)
    response = client.get(PATH)
    assert response.status_code == 200, "Some data were obtained"
    assert len(response.json()) == 1, "There is only one driver in the database"
