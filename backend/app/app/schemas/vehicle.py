from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr


class VehicleBase(BaseModel):
    """Basic information about the vehicle."""
    make: str
    model: str
    plate_number: constr(regex="^[A-Z]{2}\s\d{4}\s[A-Z]{2}$")  # example "AA 1234 OO"


class VehicleCreate(VehicleBase):
    """Used when creating a vehicle record in the database."""
    pass


class VehicleUpdate(VehicleBase):
    """Used when updating the information about the vehicle in the database."""
    driver_id: Optional[int]


class VehicleDatabase(VehicleBase):
    """Vehicle information obtained from the database."""
    id: int
    driver_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: datetime.strftime(dt, "%d/%m/%Y %H:%M:%S")
        }
