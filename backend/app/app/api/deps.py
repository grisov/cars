from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Generator:
    """Return a database session and close it when the operation is complete."""
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()
