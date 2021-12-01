from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/vehicle/", response_model=List[schemas.VehicleDatabase])
def get_all_vehicles(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        vehicles = crud.vehicle.get_multi(db, limit=crud.vehicle.count(db))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no vehicles in the database"
        )
    return [schemas.VehicleDatabase(**jsonable_encoder(vehicle)) for vehicle in vehicles]
