import connexion
from api.models.course import Course
from api.models.error import Error
from api.utils import Data


def add_get(name=None, start=None, end=None, amount=None):
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
    :rtype: Course
    """
    start = Data(start).deserialize_date()
    end = Data(end).deserialize_date()
    return 'do some magic!'


def add_post(course):
    """Add new course via a request body.
    Add a new training course to the database using POST-method.
    :param course: A set of data describing the training course
    :type course: dict | bytes
    :rtype: Course
    """
    if connexion.request.is_json:
        course = Course.from_dict(connexion.request.get_json())
    return 'do some magic!'
