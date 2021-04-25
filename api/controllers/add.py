import connexion
from typing import Tuple, Optional, Union
from api.models.course import Course
from api.models.error import Error
from api.database import Database


def add_get(name: str, start: str, end: str, amount: int) -> Union[Union[Course, Error, None], Tuple]:
    """Add new course via a URL parameter.
    Add a new training course to the database using GET-method.
    :param name: Name of the training course
    :type name: str
    :param start: Start date of the training course
    :type start: str
    :param end: End date of the training course
    :type end: str
    :param amount: Number of lectures that make up the training course
    :type amount: int
    :return: the training course that has been added to the database
    :rtype: Union[Course, Error, None]
    """
    try:
        course = Course(name, start, end, amount)
    except (ValueError, TypeError) as err:
        return Error(
            status=400,
            title="Bad Request",
            detail=str(err)
        ), 400
    with Database() as db:
        record = db.add(course)
    return record


def add_post(course: Optional[Course]=None) -> Union[Union[Course, Error, None], Tuple]:
    """Add new course via a request body.
    Add a new training course to the database using POST-method.
    :param course: the data describing the training course
    :type course: Optional[Course]
    :return: the training course that has been added to the database
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
        record = db.add(course)
    return record
