from random import randint
from sqlalchemy.orm import Session
from app import crud, schemas
from .rand import random_lower_string, random_plate_number


def create_drivers(db: Session) -> int:
    """Create a random set of drivers in the database.
    :param db: database connection session
    :return: the number of created drivers
    """
    count = randint(20, 100)
    for i in range(count):
        first_name = random_lower_string()
        last_name = random_lower_string()
        driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
        crud.driver.create(db, obj_in=driver_in)
    return count


def create_vehicles(db: Session, with_driver: bool) -> int:
    """Create a random set of vehicles in the database
    if necessary, also create drivers and add them to vehicles.
    :param db: database connection session
    :param with_driver: sign of the presence of the driver in the car
    :return: the number of created vehicles
    """
    count = randint(20, 100)
    for i in range(count):
        driver_id = None 
        if with_driver:
            first_name = random_lower_string()
            last_name = random_lower_string()
            driver_in = schemas.DriverCreate(first_name=first_name, last_name=last_name)
            driver_id = crud.driver.create(db, obj_in=driver_in).id
        make = random_lower_string()
        model = random_lower_string()
        plate_number = random_plate_number()
        vehicle_in = schemas.VehicleCreate(make=make, model=model, plate_number=plate_number)
        crud.vehicle.create(db, obj_in=vehicle_in, driver_id=driver_id)
    return count
