from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, PositiveInt, validator


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
    id: PositiveInt
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: datetime.strftime(dt, "%d/%m/%Y %H:%M:%S")
        }


class CreatedAt(BaseModel):
    """Query parameters for filtering drivers by registration dates."""
    gte: Optional[date] = None
    lte: Optional[date] = None

    @validator('*', pre=True)
    def validate_input_date_format(cls, value):
        if value is None:
            return value
        return datetime.strptime(value, "%d-%m-%Y").date()


class DriverID(BaseModel):
    driver_id: Optional[PositiveInt] = None
