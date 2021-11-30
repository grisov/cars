from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.base_class import Base


class Driver(Base):
    """Information about the drivers of the vehicle."""
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
