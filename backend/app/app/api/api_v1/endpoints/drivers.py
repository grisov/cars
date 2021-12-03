from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, status
from fastapi.encoders import jsonable_encoder
from pydantic import PositiveInt, ValidationError
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    path="/driver/",
    response_model=List[schemas.DriverDatabase],
    summary="Get the list of drivers from the database",
    description="The list of drivers can be filtered by registration date")
async def get_drivers(
    created_at__gte: Optional[str] = Query(default=None, regex="^\d{1,2}-\d{1,2}-\d{4}$", title="Start date"),
    created_at__lte: Optional[str] = Query(default=None, regex="^\d{1,2}-\d{1,2}-\d{4}$", title="End date"),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get a list of drivers, filtered by date of registration if nesesery.
    :param created_at__gte: registration starting from this date (inclusive)
    :param created_at__lte: registration before this date
    """
    try:
        created_at = schemas.CreatedAt(gte=created_at__gte, lte=created_at__lte)
    except (ValueError, ValidationError) as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The date must be in DD-MM-YYYY format: %s" % str(ve)
        )
    try:
        drivers = crud.driver.get_filtered(db, gte=created_at.gte, lte=created_at.lte)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not drivers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no drivers in the database that meet the specified criteria."
        )
    return [schemas.DriverDatabase(**jsonable_encoder(driver)) for driver in drivers]


@router.get(
    path="/driver/{driver_id}/",
    response_model=schemas.DriverDatabase,
    summary="Detailed information about the driver",
    description="Get complete information about the driver by his ID from the database")
async def get_driver_by_id(
    driver_id: PositiveInt = Path(..., title=""),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get detailed information about the driver.
    :param driver_id: driver ID in the database
    """
    try:
        driver = crud.driver.get(db, id=driver_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with ID={driver_id} is not found in the database"
        )
    return schemas.DriverDatabase(**jsonable_encoder(driver))


@router.post(
    path="/driver/",
    response_model=schemas.DriverDatabase,
    summary="Add new driver",
    description="Create a new driver in the database")
async def add_driver(
    driver_in: schemas.DriverCreate = Body(..., title=""),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Add new driver to the database.
    :param driver_in: detailed information about the driver
    """
    try:
        driver = crud.driver.create(db, obj_in=driver_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.DriverDatabase(**jsonable_encoder(driver))


@router.patch(
    path="/driver/{driver_id}/",
    response_model=schemas.DriverDatabase,
    summary="Update driver information",
    description="Update driver details with specified ID")
async def update_driver(
    driver_id: PositiveInt = Path(..., title=""),
    driver_in: schemas.DriverUpdate = Body(..., title=""),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Update the driver details.
    :param driver_id: driver ID in the database
    :param driver_in: new details about the driver
    """
    try:
        driver = crud.driver.get(db, id=driver_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with ID={driver_id} is not found in the database"
        )
    try:
        updated_driver = crud.driver.update(db, db_obj=driver, obj_in=driver_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.DriverDatabase(**jsonable_encoder(updated_driver))


@router.delete(
    path="/driver/{driver_id}/",
    response_model=schemas.DriverDatabase,
    summary="Delete the driver",
    description="Remove the driver with the specified ID from the database")
async def delete_driver(
    driver_id: PositiveInt = Path(..., title=""),
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Delete the driver from the database.
    :param driver_id: driver ID in the database
    """
    try:
        driver = crud.driver.remove(db, id=driver_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with ID={driver_id} is not found in the database"
        )
    return schemas.DriverDatabase(**jsonable_encoder(driver))
