from datetime import date
from typing import Dict, List, Optional, Union
from api.models.base_model import Model
from api.utils import Data


class Course(Model):
    """Data structure that represents the training course."""

    def __init__(
            self,
            name: str,
            start: Union[date, str],
            end: Union[date, str],
            amount: int,
            id: Optional[int]=-1
        ) -> None:
        """Data model representing the training course.
        :param name: The name of the course
        :type name: str
        :param start: the start date of the course
        :type start: Union[date, str]
        :param end: the graduation date of the course
        :type end: Union[date, str]
        :param amount: the number of lectures that make up the course
        :type amount: int
        :param id: the index of the course in the database
        :type id: Optional[int]
        """
        self.openapi_types = {
            'name': str,
            'start': date,
            'end': date,
            'amount': int,
            'id': int
        }
        self.attribute_map = {
            'name': 'name',
            'start': 'start',
            'end': 'end',
            'amount': 'amount',
            'id': 'id'
        }
        self._name = name
        self._start = start
        self._end = end
        self._amount = amount
        self._id = id

    @property
    def name(self) -> str:
        """Get the name of this training course.
        :return: The name of the course.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set the name of the training course.
        :param name: The name of the Course.
        :type name: Optional[str]
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        elif len(name) < 2:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `2`")
        self._name = name

    @property
    def start(self) -> Union[date, str]:
        """Get the start date of the course.
        :return: The start date of the course.
        :rtype: Union[date, str]
        """
        return self._start

    @start.setter
    def start(self, start: Union[date, str, None]) -> None:
        """Set the start date of the training course.
        :param start: The start date of the course.
        :type start: Union[date, str, None]
        """
        if start is None:
            raise ValueError("Invalid value for `start`, must not be `None`")
        self._start = start

    @property
    def end(self) -> Union[date, str]:
        """Get the graduation date of the course.
        :return: The graduation date of the course
        :rtype: Union[date, str]
        """
        return self._end

    @end.setter
    def end(self, end: Union[date, str, None]) -> None:
        """Set the graduation date of the course.
        :param end: The graduation date of the course
        :type end: Union[date, str, None]
        """
        if end is None:
            raise ValueError("Invalid value for `end`, must not be `None`")
        self._end = end

    @property
    def amount(self) -> int:
        """Get the number of lectures in the training course.
        :return: the number of lectures that make up the course
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount: Optional[int]) -> None:
        """Set the number of lectures in the training course.
        :param amount: the number of lectures that make up the course
        :type amount: Optional[int]
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")
        elif amount > 255:
            raise ValueError("Invalid value for `amount`, must be a value less than or equal to `255`")
        elif amount < 1:
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `1`")
        self._amount = amount

    @property
    def id(self) -> int:
        """Get the id of the course,
        value -1 if there is no corresponding record in the DB.
        :return: The ID of the course in the DB
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: Optional[int]) -> None:
        """Set the id of the training course.
        :param id: The ID of the course in the DB
        :type id: Optional[int]
        """
        self._id = id
