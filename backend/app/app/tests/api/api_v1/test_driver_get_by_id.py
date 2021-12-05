from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings

PATH = f"{settings.API_V1_STR}/drivers/driver/"
