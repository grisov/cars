from typing import Any, List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    path="/vehicle/",
    response_model=List[schemas.VehicleDatabase],
    summary="Get vehicles list",
    description="The list of vehicles can be filtered based on the presence or absence of the driver")
def get_vehicles(
    with_drivers: Optional[Literal["yes", "no"]] = None,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get a filtered list of the vehicles.
    :param with_drivers: a sign of the presence or absence of a driver in the vehicle
    """
    try:
        vehicles = crud.vehicle.get_filtered(db, with_driver=with_drivers)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not vehicles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no vehicles in the database that meet the specified criteria"
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
def add_vehicle(
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


@router.patch("/vehicle/{vehicle_id}/", response_model=schemas.VehicleDatabase)
def update_vehicle(
    vehicle_id: int,
    vehicle_in: schemas.VehicleUpdate,
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
    try:
        updated_vehicle = crud.vehicle.update(db, db_obj=vehicle, obj_in=vehicle_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.VehicleDatabase(**jsonable_encoder(updated_vehicle))


@router.delete("/vehicle/{vehicle_id}/", response_model=schemas.VehicleDatabase)
def delete_vehicle(
    vehicle_id: int,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        vehicle = crud.vehicle.remove(db, id=vehicle_id)
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
