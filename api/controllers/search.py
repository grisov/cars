import connexion
from typing import List
from api.models.course import Course
from api.models.error import Error
from api.models.search_data import SearchData
from api.utils import Data


def search_get(name=None, start=None, end=None):
    """Searching of courses on the properties specified in URL.
    Search for a training course by name or filter the list by specified dates.
    :param name: Name of the training course
    :type name: str
    :param start: Start date of the training course
    :type start: str
    :param end: End date of the training course
    :type end: str
    :rtype: List[Course]
    """
    start = Data(start).deserialize_date()
    end = Data(end).deserialize_date()
    return 'do some magic!'


def search_post(search_data=None):
    """Searching of courses on the properties specified in request body.
    Search for a training course by name or filter the list by specified dates.
    :param search_data: Course name to search for or dates to filter the results
    :type search_data: dict | bytes
    :rtype: List[Course]
    """
    if connexion.request.is_json:
        search_data = SearchData.from_dict(connexion.request.get_json())
    return 'do some magic!'
