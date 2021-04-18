from datetime import date
from typing import Dict, List, Optional, Union
from api.models.base_model import Model


class Course(Model):
    """Data structure that represents the training course."""

    def __init__(
            self,
            name: str="--",
            start: Union[date, str]="1970-01-01",
            end: Union[date, str]="1970-01-01",
            amount: int=1,
            id: int=-1
        ) -> None:
        """Data model representing the training course.
        :param n	ame: The name of the course
        	:type name: str	
        :param start: the start date of the course
        :type start: Union[date, str]
        :param end: the graduation date of the course
        :type end: Union[date, str]
        :param amount: the number of lectures that make up the course
        :type amount: int
        :param id: the index of the course in the database
        :type id: int
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
        self.name = name
        self.start = start
        self.end = end
        self.amount = amount
        self.id = id

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
        self._name = self.validate_name(name)

    @property
    def start(self) -> date:
        """Get the start date of the course.
        :return: The start date of the course.
        :rtype: date
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
        self._start = self.validate_date(start)

    @property
    def end(self) -> date:
        """Get the graduation date of the course.
        :return: The graduation date of the course
        :rtype: date
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
        self._end = self.validate_date(end)

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
        self._amount = self.validate_amount(amount)

    @property
    def id(self) -> int:
        """Get the id of the course,
        value -1 if there is no corresponding record in the DB.
        :return: The ID of the course in the DB
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        """Set the id of the training course.
        :param id: The ID of the course in the DB
        :type id: int
        """
        self._id = id

    def to_str(self) -> str:
        """Return the string representation of the search model.
        :return: the string representation
        :rtype: str
        """
        data: Dict = dict(self.to_dict())
        if data.get('start'):
            data['start'] = str(data['start'])
        if data.get('end'):
            data['end'] = str(data['end'])
        return str(data)
