from fastapi import APIRouter
from .endpoints import drivers, vehicles

api_router = APIRouter()

api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
