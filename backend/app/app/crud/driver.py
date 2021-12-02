from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.models import Driver
from app.schemas import DriverCreate, DriverUpdate
from .base import CRUDBase


class CRUDDriver(CRUDBase[Driver, DriverCreate, DriverUpdate]):
    """CRUD object with basic methods for manipulation of the drivers records in a database."""

    def get_filtered(
        self,
        db: Session,
        *,
        gte: Optional[date] = None,
        lte: Optional[date] = None
    ) -> List[Driver]:
        """Get a list of drivers filtered by registration date.
        :param gte: start date
        :param lte: end date
        (if any of these values is empty, it is not taken into account)
        """
        query = db.query(Driver)
        if gte is not None:
            query = query.filter(Driver.created_at >= datetime.fromordinal(gte.toordinal()))
        if lte is not None:
            query = query.filter(Driver.created_at < datetime.fromordinal(lte.toordinal()))
        return query.all()


driver = CRUDDriver(Driver)
