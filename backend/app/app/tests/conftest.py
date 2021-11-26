from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as cl:
        yield cl
