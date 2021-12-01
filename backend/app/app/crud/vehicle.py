from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleUpdate
from .base import CRUDBase


class CRUDVehicle(CRUDBase[Vehicle, VehicleCreate, VehicleUpdate]):
    """CRUD object with basic methods for manipulation of the vehicles records in a database."""

    def create(
        self,
        db: Session,
        *,
        obj_in: VehicleCreate,
        driver_id: Optional[int] = None
    ) -> Vehicle:
        """Add a new vehicle object to the database."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, driver_id=driver_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


vehicle = CRUDVehicle(Vehicle)
