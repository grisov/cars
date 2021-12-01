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


@router.get("/vehicle/{vehicle_id}/", response_model=schemas.VehicleDatabase)
def get_vehicle_by_id(
    vehicle_id: int,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        vehicle = crud.vehicle.get(db, id=vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID={vehicle_id} is not found in the database"
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))


@router.post("/vehicle/", response_model=schemas.VehicleDatabase)
def add_vehicle_to_db(
    vehicle_in: schemas.VehicleCreate,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))
