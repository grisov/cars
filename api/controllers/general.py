import connexion
from api.models.course import Course
from api.models.error import Error


def get_details(id):
    """Detailed information about the training course.
    Complete information about the training course with the specified ID.
    :param id: The ID of the Training course in the database
    :type id: int
    :rtype: Course
    """
    return 'do some magic!'


def remove(id):
    """Delete a course with the specified ID.
    Delete a training course from the database.
    :param id: The ID of the Training course in the database
    :type id: int
    :rtype: Course
    """
    return 'do some magic!'


def update(id, course=None):
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
