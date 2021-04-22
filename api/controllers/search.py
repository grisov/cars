import connexion
from typing import List, Union, Optional
from api.models.course import Course
from api.models.error import Error
from api.models.search_data import SearchData
from api.database import Database


def search_get(
        name: Optional[str]=None,
        start: Optional[str]=None,
        end: Optional[str]=None
    ) -> Union[List[Course], Error]:
    """Searching of courses on the properties specified in URL.
    Search for a training course by name or filter the list by specified dates.
    :param name: part of the name of the training course
    :type name: Optional[str]
    :param start: Start date of the training courses
    :type start: Optional[str]
    :param end: End date of the training courses
    :type end: Optional[str]
    :return: the list of courses that meet the search criteria
    :rtype: Union[List[Course], Error]
    """
    try:
        query = SearchData(name, start, end)
    except (ValueError, TypeError) as err:
        return Error(
            status=400,
            title="Bad Request",
            detail=str(err)
        ), 400
    with Database() as db:
        result = db.search(query)
    return result


def search_post(search_data: Optional[SearchData]=None) -> Union[List[Course], Error]:
    """Searching of courses on the properties specified in request body.
    Search for a training course by name or filter the list by specified dates.
    :param search_data: Course name to search for or dates to filter the results
    :type search_data: Optional[SearchData]
    :return: the list of courses that meet the search criteria
    :rtype: Union[List[Course], Error]
    """
    try:
        if connexion.request.is_json:
            query = SearchData.from_dict(connexion.request.get_json())
        else:
            raise ValueError("Wrong data format in request body")
    except (ValueError, TypeError) as err:
        return Error(
            status=400,
            title="Bad Request",
            detail=str(err)
        ), 400
    with Database() as db:
        result = db.search(query)
    return result
