from __future__ import annotations
from datetime import date
from typing import Dict, Union, Optional
from api.utils import Data


class Model(object):
    # openapiTypes: The key is attribute name
    # and the value is attribute type.
    openapi_types = {}

    # attributeMap: The key is attribute name
    # and the value is json key in definition.
    attribute_map = {}

    @classmethod
    def from_dict(cls, dikt: Dict):
        """Return the dict as a model.
        :param dikt: the dict with the required attribute names and their values
        :type dikt: Dict
        :return: the object inherited from Model
        :rtype: Model
        """
        return Data(dikt).deserialize_model(cls)

    def to_dict(self) -> Dict:
        """Return the model properties as a dict.
        :return: presentation of the data model in the dict form
        :rtype: Dict
        """
        result = {}
        for attr in self.openapi_types:
            value = getattr(self, attr)
            if value is None:
                continue
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        return result

    def to_str(self) -> str:
        """Return the string representation of the model.
        :return: the string representation
        :rtype: str
        """
        return str(self.to_dict())

    def __repr__(self) -> str:
        """Represent a model object as a string.
        :return: the string representation
        :rtype: str
        """
        return self.to_str()

    def __eq__(self, other: Model) -> bool:
        """Return true if both objects are equal.
        :param other: another Model object
        :type other: Model
        :return: the result of comparing objects for equality
        :rtype: bool
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other: Model) -> bool:
        """Return true if both objects are not equal.
        :param other: another Model object
        :type other: Model
        :return: the result of comparing objects for inequality
        :rtype: bool
        """
        return not self == other

    @staticmethod
    def validate_name(name: Optional[str]) -> Optional[str]:
        """Validation of the passed value for the course name.
        :param name: the name of the training course
        :type name: Optional[str]
        :return: the validated value of the course name
        :rtype: Optional[name]
        """
        if name is not None and type(name) != str:
            raise TypeError("Invalid value type for `name`, type must be `str`")
        elif name is not None and len(name) < 2:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `2`")
        return name

    @staticmethod
    def validate_date(dt: Union[date, str, None]) -> Optional[date]:
        """Validation of the passed value for the date.
        :param dt: the date
        :type dt: Union[date, str, None]
        :return: the validated value of the date
        :rtype: Optional[date]
        """
        if dt is not None and isinstance(dt, str):
            dt = Data(dt).deserialize(date)
            if type(dt) != date:
                raise ValueError("The date must be in ISO format like `2021-04-28`")
        if dt is not None and type(dt) != date:
            raise TypeError("Invalid value type, it must be `date` or `str`")
        return dt

    @staticmethod
    def validate_amount(amount: Optional[int]) -> Optional[int]:
        """Validation of the passed value for the course amount.
        :param amount: the number of lectures that make up the course
        :type amount: Optional[int]
        :return: the validated value of the course amount
        :rtype: Optional[int]
        """
        if amount is not None and type(amount) != int:
            amount = Data(amount).deserialize(int)
            if type(amount) != int:
                raise TypeError("Invalid value type for `amount`, it must be `int`")
        if amount is not None and amount < 1:
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `1`")
        elif amount is not None and amount > 255:
            raise ValueError("Invalid value for `amount`, must be a value less than or equal to `255`")
        return amount
