from __future__ import annotations
from typing import Dict
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
        """Returns the dict as a model.
        :param dikt: the dict with the required attribute names and their values
        :type dikt: Dict
        :return: the object inherited from Model
        :rtype: Model
        """
        return Data(dikt).deserialize_model(cls)

    def to_dict(self) -> Dict:
        """Returns the model properties as a dict.
        :return: presentation of the data model in the dict form
        :rtype: Dict
        """
        result = {}
        for attr in self.openapi_types:
            value = getattr(self, attr)
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
        """Returns the string representation of the model.
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
        """Returns true if both objects are equal.
        :param other: another Model object
        :type other: Model
        :return: the result of comparing objects for equality
        :rtype: bool
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other: Model) -> bool:
        """Returns true if both objects are not equal.
        :param other: another Model object
        :type other: Model
        :return: the result of comparing objects for inequality
        :rtype: bool
        """
        return not self == other
