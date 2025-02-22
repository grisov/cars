from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Basic operations on models in the database:
    Create, Read, Update, Delete (CRUD)
    """

    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(
        self,
        db: Session,
        id: Any
    ) -> Optional[ModelType]:
        """Get object from database by its ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Get a certain number of objects from the database."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        """Add a new object to the database."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        exclude_empty: bool = False
    ) -> ModelType:
        """Update the object in the database.
        :param db: database session
        :param db_obj: model object from the database
        :param obj_in: data to update
        :param exclude_empty: ignore empty values ​​when updating
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, Dict):
            update_data: Dict[str, Any] = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if exclude_empty and update_data[field] is None:
                    continue
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db: Session,
        *,
        id: int
    ) -> Optional[ModelType]:
        """Delete the object from the database."""
        obj = db.query(self.model).get(id)
        if obj is not None:
            db.delete(obj)
            db.commit()
        return obj

    def count(
        self,
        db: Session
    ) -> int:
        """Get the total number of records in the table."""
        return db.query(self.model).count()
