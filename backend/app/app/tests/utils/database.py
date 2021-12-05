from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.base import Base


def get_testing_session() -> Session:
    """Create connection session with inmemory database,
    also create all necessary tables in this database.
    """
    engine = create_engine(url="sqlite://", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    return TestingSessionLocal


def override_get_db() -> Generator:
    """Upon request return the database connection session and close it after the operation is complete."""
    try:
        database = get_testing_session()()
        yield database
    finally:
        database.close()
