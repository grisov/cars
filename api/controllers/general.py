import connexion
from typing import Union
from api.models.course import Course
from api.models.error import Error
from api.database import Database


def get_details(cid: int) -> Union[Course, Error]:
    """Detailed information about the training course.
    Complete information about the training course with the specified ID.
    :param cid: The ID of the Training course in the database
    :type cid: int
    :return: the detailed information about the training course
    :rtype: Union[Course, Error]
    """
    course = Database().get(cid)
    if course is not None:
        return course
    return Error(
            status=214,
            title="No Data",
            detail=f"There is no record with index {cid} in the database",
            type="about:blank"
        ), 214


def remove(id: int):
    """Delete a course with the specified ID.
    Delete a training course from the database.
    :param id: The ID of the Training course in the database
    :type id: int
    :rtype: Course
    """
    return 'do some magic!'


def update(id: int, course: Course=None):
    """Update a course with the specified ID.
    Change the properties of the training course in the database.
    :param id: The ID of the Training course in the database
    :type id: int
    :param course: A set of data describing the training course
    :type course: dict | bytes
    :rtype: Course
    """
    if connexion.request.is_json:
        course = Course.from_dict(connexion.request.get_json())
    return 'do some magic!'
