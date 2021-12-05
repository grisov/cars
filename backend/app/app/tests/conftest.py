from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from app.api import deps
from app.main import app
from app.tests.utils import override_get_db


@pytest.fixture(scope="module")
def client() -> Generator:
    """Test client for make requests."""
    with TestClient(app) as cl:
        yield cl


# Override the main database dependency to the testing database dependency
app.dependency_overrides[deps.get_db] = override_get_db
db = pytest.fixture(override_get_db, scope="function", name="db")
