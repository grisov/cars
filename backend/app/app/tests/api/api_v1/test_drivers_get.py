from typing import List
from datetime import datetime, timedelta
import re
from random import randint
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.tests.utils import random_lower_string, create_drivers

PATH = f"{settings.API_V1_STR}/drivers/driver/"
DATE_FORMAT = "%d-%m-%Y"


def test_drivers_get_from_empty_db_without_filtering(
    client: TestClient,
    db: Session
) -> None:
    """Check getting all drivers from the empty database without filtering."""
    response = client.get(PATH)
    assert response.status_code == 404, "There are no drivers in the database"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no drivers in the database that meet the specified criteria."


def test_get_existing_single_driver_without_filtering(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing single driver from the database without filtering."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    crud.driver.create(db, obj_in=driver)
    response = client.get(PATH)
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert isinstance(response.json(), List), "Response data type"
    assert len(response.json()) == 1, "There is only one driver in the database"


def test_response_driver_data_format(
    client: TestClient,
    db: Session
) -> None:
    """Check the format of the driver data in the response."""
    first_name = random_lower_string()
    last_name = random_lower_string()
    driver = schemas.DriverCreate(first_name=first_name, last_name=last_name)
    crud.driver.create(db, obj_in=driver)
    response = client.get(PATH)
    # Validation of user information
    rec = response.json()[0]
    assert rec["first_name"] == first_name, "First name of the driver"
    assert rec["last_name"] == last_name, "Last name of the driver"
    assert rec["id"] > 0, "Driver ID in the database"
    assert rec["created_at"] is not None, "Date the driver was added to the database"
    assert rec["updated_at"] is not None, "Driver information update date"
    # Check the datetime format in the response
    assert re.match("^\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}$", rec["created_at"]), "The format of the creation date"
    assert re.match("^\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}$", rec["updated_at"]), "The update date format"


def test_get_many_drivers_without_filtering(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing many drivers from the database without filtering."""
    number = randint(10, 50)
    for i in range(number):
        first_name = random_lower_string()
        last_name = random_lower_string()
        driver = schemas.DriverCreate(first_name=first_name, last_name=last_name)
        crud.driver.create(db, obj_in=driver)
    response = client.get(PATH)
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert isinstance(response.json(), List), "Response data type"
    assert len(response.json()) == number, "Number of drivers in the database"


def test_get_drivers_created_at_filter_gte_yesterday(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created after the specified date (yesterday)."""
    number = create_drivers(db)
    dt = datetime.now() - timedelta(days=2)
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__gte={dt_str}")
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert len(response.json()) == number, "All drivers are created later than yesterday"


def test_get_drivers_created_at_filter_gte_today(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created after the specified date (today)."""
    number = create_drivers(db)
    dt = datetime.now()
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__gte={dt_str}")
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert len(response.json()) == number, "Today's creation date is included"


def test_get_drivers_created_at_filter_gte_tomorrow(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created after the specified date (tomorrow)."""
    number = create_drivers(db)
    dt = datetime.now() + timedelta(days=1)
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__gte={dt_str}")
    assert response.status_code == 404, "All drivers added today do not meet the condition"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no drivers in the database that meet the specified criteria."


def test_get_drivers_created_at_gte_wrong_format(
    client: TestClient,
    db: Session
) -> None:
    """The 'created_at__gte' parameter is in the wrong format."""
    dt = datetime.now()
    for dt_str in [dt.isoformat(), "hello", "123", "12 Sep 21", "07/03/2017", "23:10:22", None]:
        response = client.get(f"{PATH}?created_at__gte={dt_str}")
        assert response.status_code == 422, "Incorrect parameters format"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_get_drivers_created_at_filter_lte_yesterday(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created before the specified date (yesterday)."""
    number = create_drivers(db)
    dt = datetime.now() - timedelta(days=1)
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__lte={dt_str}")
    assert response.status_code == 404, "All drivers added today do not meet the condition"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no drivers in the database that meet the specified criteria."


def test_get_drivers_created_at_filter_lte_today(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created before the specified date (today)."""
    number = create_drivers(db)
    dt = datetime.now()
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__lte={dt_str}")
    assert response.status_code == 404, "All drivers added today do not meet the condition"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert "detail" in response.json(), "Detailed description of the response"
    assert response.json()["detail"] == "There are no drivers in the database that meet the specified criteria."


def test_get_drivers_created_at_filter_lte_tomorrow(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created before the specified date (tomorrow)."""
    number = create_drivers(db)
    dt = datetime.now() + timedelta(days=2)
    dt_str = datetime.strftime(dt, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__lte={dt_str}")
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert len(response.json()) == number, "All drivers are created before tomorrow"


def test_get_drivers_created_at_lte_wrong_format(
    client: TestClient,
    db: Session
) -> None:
    """The 'created_at__lte' parameter is in the wrong format."""
    dt = datetime.now()
    for dt_str in [dt.isoformat(), "hello", "123", "12 Sep 21", "07/03/2017", "23:10:22", None]:
        response = client.get(f"{PATH}?created_at__lte={dt_str}")
        assert response.status_code == 422, "Incorrect parameters format"
        assert response.headers["Content-Type"] == "application/json", "Response content type"
        assert "detail" in response.json(), "Detailed description of the response"


def test_get_drivers_created_at_filter_gte_and_lte(
    client: TestClient,
    db: Session
) -> None:
    """Check getting existing drivers created in a given period of time."""
    number = create_drivers(db)
    dt = datetime.now()
    gte = dt - timedelta(days=2)
    lte = dt + timedelta(days=2)
    gte_str = datetime.strftime(gte, DATE_FORMAT)
    lte_str = datetime.strftime(lte, DATE_FORMAT)
    response = client.get(f"{PATH}?created_at__gte={gte_str}&created_at__lte={lte_str}")
    assert response.status_code == 200, "The request was completed successfully"
    assert response.headers["Content-Type"] == "application/json", "Response content type"
    assert isinstance(response.json(), List), "Response data type"
    assert len(response.json()) == number, "All drivers were added within the specified period"
