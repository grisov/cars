from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from .driver import Driver


class Vehicle(Base):
    """Information about the vehicles."""
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    plate_number = Column(String(10), nullable=False)  # "AA 1234 OO"
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    driver = relationship("Driver", backref="vehicle", uselist=False)
