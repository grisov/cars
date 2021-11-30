from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Vehicle(Base):
    """Information about the vehicles."""
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    make = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    plate_number = Column(String(10), nullable=False)  # "AA 1234 OO"
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    driver = relationship("Driver", backref="vehicle", uselist=False)
