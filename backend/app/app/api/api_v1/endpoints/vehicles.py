from typing import Any, List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import PositiveInt
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


@router.get(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Vehicle information",
    description="Get detailed information about a particular vehicle by its ID")
def get_vehicle_by_id(
    vehicle_id: PositiveInt,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get detailed information about the vehicle.
    :param vehicle_id: vehicle ID in the database
    """
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


@router.post(
    path="/vehicle/",
    response_model=schemas.VehicleDatabase,
    summary="Add new vehicle",
    description="Create a new vehicle in the database")
def add_vehicle(
    vehicle_in: schemas.VehicleCreate,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Create a new vehicle in the database.
    :param vehicle_in: information about the vehicle to be added to the database
    """
    try:
        vehicle = crud.vehicle.create(db, obj_in=vehicle_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.VehicleDatabase(**jsonable_encoder(vehicle))


@router.patch(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Update vehicle information",
    description="Update vehicle details in the database")
def update_vehicle(
    vehicle_id: PositiveInt,
    vehicle_in: schemas.VehicleUpdate,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Update vehicle details in the database.
    :param vehicle_id: vehicle ID in the database
    :param vehicle_in: new vehicle information to be updated in the database
    """
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


@router.delete(
    path="/vehicle/{vehicle_id}/",
    response_model=schemas.VehicleDatabase,
    summary="Delete the vehicle",
    description="Remove the specified vehicle from the database")
def delete_vehicle(
    vehicle_id: PositiveInt,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Delete the specified vehicle from the database.
    :param vehicle_id: vehicle ID in the database
    """
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
