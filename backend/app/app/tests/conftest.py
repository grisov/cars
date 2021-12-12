from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from app.api import deps
from app.db.base import Base
from app.main import app


@pytest.fixture(scope="session")
def engine() -> Generator:
    """Create the SQLite test database with all nesesery tables in memory."""
    engine = create_engine(url="sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(engine: Engine) -> Generator:
    """Create a separate transaction for each test function."""
    connection = engine.connect()
    # Begin a non-ORM transaction
    connection.begin()
    # Bind an individual Session to the connection
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db: Session) -> Generator:
    """Test client for make requests."""
    app.dependency_overrides[deps.get_db] = lambda: db
    with TestClient(app) as cl:
        yield cl
