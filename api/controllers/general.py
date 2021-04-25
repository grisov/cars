import connexion
from typing import Tuple, Union, Optional
from api.models.course import Course
from api.models.error import Error
from api.database import Database


def get_details(cid: int) -> Union[Union[Course, Error, None], Tuple]:
    """Detailed information about the training course with the specified ID.
    :param cid: The ID of the Training course in the database
    :type cid: int
    :return: the detailed information about the training course
    :rtype: Union[Course, Error, None]
    """
    with Database() as db:
        course = db.get(cid)
    if course is not None:
        return course
    return Error(
        status=204,
        title="No Content",
        detail=f"There is no record with index {cid} in the database"
    ), 204


def remove(cid: int) -> Union[Union[Course, Error, None], Tuple]:
    """Delete a course with the specified ID from DB.
    :param cid: The ID of the Training course in the database
    :type cid: int
    :return: the detailed information about the deleted course
    :rtype: Union[Course, Error, None]
    """
    with Database() as db:
        course = db.remove(cid)
    if course is not None:
        return course
    return Error(
        status=204,
        title="No Content",
        detail=f"There is no record with index {cid} in the database"
    ), 204


def update(cid: int, course: Optional[Course] = None) -> Union[Union[Course, Error, None], Tuple]:
    """Update the properties of the training course in the DB.
    :param cid: The ID of the Training course in the database
    :type cid: int
    :param course: new training course data for replacement
    :type course: Optional[Course]
    :return: the updated information about the course
    :rtype: Union[Course, Error, None]
    """
    try:
        if connexion.request.is_json:
            course = Course.from_dict(connexion.request.get_json())
        else:
            raise ValueError("Wrong data format in request body")
    except (ValueError, TypeError) as err:
        return Error(
            status=400,
            title="Bad Request",
            detail=str(err)
        ), 400
    with Database() as db:
        record = db.update(cid, course)
    return record
