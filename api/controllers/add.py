import connexion
from typing import Union
from api.models.course import Course
from api.models.error import Error
from api.database import Database


def add_get(name: str, start: str, end: str, amount: int) -> Union[Course, Error]:
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
    :rtype: Union[Course, Error]
    """
    course = Course(name, start, end, amount)
    db = Database()
    record = db.add(course)
    db.close()
    return record


def add_post(course: Course=None) -> Union[Course, Error]:
    """Add new course via a request body.
    Add a new training course to the database using POST-method.
    :param course: the data describing the training course
    :type course: Course
    :return: the training course that has been added to the database
    :rtype: Union[Course, Error]
    """
    if connexion.request.is_json:
        course = Course.from_dict(connexion.request.get_json())
        db = Database()
        record = db.add(course)
        db.close()
        return record
    return Error(
            status=400,
            title="Bad Request",
            detail="Invalid data format transmitted.",
            type="about:blank"
        ), 400
