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
