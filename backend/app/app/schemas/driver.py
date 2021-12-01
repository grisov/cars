from datetime import datetime
from pydantic import BaseModel


class DriverBase(BaseModel):
    """Basic information about the driver."""
    first_name: str
    last_name: str

    class Config:
        min_anystr_length = 1


class DriverCreate(DriverBase):
    """Used when creating a driver record in the database."""
    pass


class DriverUpdate(DriverBase):
    """Used when updating the information about the driver in the database."""
    pass


class DriverDatabase(DriverBase):
    """Driver information obtained from the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: datetime.strftime(dt, "%d/%m/%Y %H:%M:%S")
        }
