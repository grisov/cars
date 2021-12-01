from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DriverBase(BaseModel):
    """Basic information about the driver."""
    first_name: str
    last_name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DriverCreate(DriverBase):
    """Used when creating a driver record in the database."""
    pass


class DriverUpdate(DriverBase):
    """Used when updating the information about the driver in the database."""
    pass


class DriverDatabase(DriverBase):
    """Driver information obtained from the database."""
    id: int
