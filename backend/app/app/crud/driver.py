from sqlalchemy.orm import Session
from app.models import Driver
from app.schemas import DriverCreate, DriverUpdate
from .base import CRUDBase


class CRUDDriver(CRUDBase[Driver, DriverCreate, DriverUpdate]):
    """CRUD object with basic methods for manipulation of the drivers records in a database."""
    pass


driver = CRUDDriver(Driver)
