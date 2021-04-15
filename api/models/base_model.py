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
        """Returns the dict as a model."""
        return Data(dikt).deserialize_model(cls)

    def to_dict(self) -> Dict:
        """Returns the model properties as a dict.
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
        :rtype: str
        """
        return str(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`."""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal."""
        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal."""
        return not self == other
