from datetime import date
from typing import Dict, List, Optional, Union
from api.models.base_model import Model


class SearchData(Model):
    """Representation of the data structure for searching the course."""

    def __init__(
            self,
            name: Optional[str]=None,
            start: Union[date, str, None]=None,
            end: Union[date, str, None]=None
        ) -> None:
        """The data model defined in OpenAPI.
        :param name: The course name for searching
        :type name: Optional[str]
        :param start: the course start date for searching
        :type start: Union[date, str, None]
        :param end: the course graduation date for searching
        :type end: Union[date, str, None]
        """
        self.openapi_types = {
            'name': str,
            'start': date,
            'end': date
        }
        self.attribute_map = {
            'name': 'name',
            'start': 'start',
            'end': 'end'
        }
        self._name = name
        self._start = start
        self._end = end

    @property
    def name(self) -> Optional[str]:
        """Get the course name for searching.
        :return: The name of the course for searching
        :rtype: Optional[str]
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set the course name for searching.
        :param name: the name of the course for searching
        :type name: Optional[str]
        """
        if name is not None and len(name) < 2:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `2`")
        self._name = name

    @property
    def start(self) -> Union[date, str, None]:
        """Get the start date of the course for searching.
        :return: the start date of the course for searching
        :rtype: Union[date, str, None]
        """
        return self._start

    @start.setter
    def start(self, start: Union[date, str, None]) -> None:
        """Set the start date of the course for searching.
        :param start: the start date of the course for searching
        :type start: Union[date, str, None]
        """
        self._start = start

    @property
    def end(self) -> Union[date, str, None]:
        """Get the graduation date of the course for searching.
        :return: the graduation date of the course for searching
        :rtype: Union[date, str, None]
        """
        return self._end

    @end.setter
    def end(self, end: Union[date, str, None]) -> None:
        """Set the graduation date of the course for searching.
        :param end: the graduation date of the course for searching
        :type end: Union[date, str, None]
        """
        self._end = end
