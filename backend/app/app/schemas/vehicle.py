from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VehicleBase(BaseModel):
    """Basic information about the vehicle."""
    make: str
    model: str
    plate_number: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class VehicleCreate(VehicleBase):
    """Used when creating a vehicle record in the database."""
    pass


class VehicleUpdate(VehicleBase):
    """Used when updating the information about the vehicle in the database."""
    pass


class VehicleDatabase(VehicleBase):
    """Vehicle information obtained from the database."""
    id: int
    driver_id: Optional[int]
