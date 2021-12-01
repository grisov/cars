from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/driver/", response_model=List[schemas.DriverDatabase])
def get_all_drivers(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        drivers = crud.driver.get_multi(db, limit=crud.driver.count(db))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    if not drivers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no drivers in the database"
        )
    return [schemas.DriverDatabase(**jsonable_encoder(driver)) for driver in drivers]


@router.get("/driver/{driver_id}/", response_model=schemas.DriverDatabase)
def get_driver_by_id(
    driver_id: int,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
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


@router.post("/driver/", response_model=schemas.DriverDatabase)
def add_driver(
    driver_in: schemas.DriverCreate,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        driver = crud.driver.create(db, obj_in=driver_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to the database: %s" % str(e)
        )
    return schemas.DriverDatabase(**jsonable_encoder(driver))


@router.patch("/driver/{driver_id}/", response_model=schemas.DriverDatabase)
def update_driver(
    driver_id: int,
    driver_in: schemas.DriverUpdate,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
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
