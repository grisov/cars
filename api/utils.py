from typing import Any, Dict, List, Union, Optional, Type
from datetime import date, datetime


class GenericType(object):
    """Definition of some kinds of generic types."""

    def __init__(self, data_type: Type) -> None:
        """Initialization of the class properties.
        :param data_type: any data type
        :type data_type: Type
        """
        self._value = data_type

    @property
    def value(self) -> Type:
        """Get the original type.
        :return: the original type
        :rtype: Type
        """
        return self._value

    def is_generic(self) -> bool:
        """ Determine whether input data type is a generic type.
        :return: an indication of whether the data type is generic
        :rtype: bool
        """
        return hasattr(self.value, '__origin__')

    def is_dict(self) -> bool:
        """ Determine whether generic type is a Dict.
        :return: an indication of whether the data type is generic Dict
        :rtype: bool
        """
        return getattr(self.value, '__origin__', None) == dict

    def is_list(self) -> bool:
        """ Determine whether generic type is a List.
        :return: an indication of whether the data type is generic List
        :rtype: bool
        """
        return getattr(self.value, '__origin__', None) == list


class Data(object):
    """A set of methods for determining the type of data obtained and their deserialization."""

    def __init__(self, value: Any) -> None:
        """Data initialization.
        :param value: the input data of any type
        :type value: Any
        """
        self._primitive_types = (int, float, str, bool, bytearray)
        self._value = value

    @property
    def value(self) -> Any:
        """Get the original value of the input data.
        :return: the original value
        :rtype: Any
        """
        return self._value

    def deserialize_primitive(self, target: Union[int, float, str, bool, bytearray]) -> Union[int, float, str, bool, bytearray]:
        """Deserialize the data to the specified primitive type.
        :param target: the target data type
        :type target: Union[int, float, str, bool, bytearray]
        :return: the data that converted to the specified type
        :rtype: Union[int, float, str, bool, bytearray]
        """
        try:
            value = target(self.value)
        except UnicodeEncodeError:
            import six
            value = six.u(self.value)
        except (TypeError, ValueError):
            value = self.value
        return value

    def deserialize_object(self) -> object:
        """Return an original value.
        :return: the original value
        :rtype: object
        """
        return self.value

    def deserialize_date(self) -> Union[date, str]:
        """Deserialize ISO formated date string to datetime.date.
        Example of the ISO date format: 2021-04-27
        :return: datetime.date object
        :rtype: Union[date, str]
        """
        try:
            return datetime.strptime(self.value, "%Y-%m-%d")
        except (ValueError, TypeError):
            return self.value

    def deserialize_datetime(self) -> Union[datetime, str]:
        """Deserialize ISO formated string to datetime object.
        The string should be in iso8601 datetime format.
        Example: 2021-05-17T17:07:41
        :return: the datetime object
        :rtype: Union[datetime, str]
        """
        try:
            return datetime.strptime(self.value, "%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            return self.value

    def deserialize(self, target: object) -> Optional[object]:
        """Try to deserialize any type into an object.
        :param target: the target data type
        :type target: object
        :return: deserialized data
        :rtype: Optional[object]
        """
        if self.value is None:
            return None
        if target in self._primitive_types:
            return self.deserialize_primitive(target)
        elif target == object:
            return self.deserialize_object()
        elif target == date:
            return self.deserialize_date()
        elif target == datetime:
            return self.deserialize_datetime()
        elif GenericType(target).is_generic():
            if GenericType(target).is_list():
                return self.deserialize_list(target.__args__[0])
            if GenericType(target).is_dict():
                return self.deserialize_dict(target.__args__[1])
        else:
            return self.deserialize_model(target)

    def deserialize_model(self, target: Union[Dict, List]) -> object:
        """Deserialize list or dict to model.
        :param target: the target data model object
        :type target: Union[Dict, List]
        :return: the data model object
        :rtype: api.models.base_model.Model
        """
        instance = target()
        if not instance.openapi_types:
            return self.value
        for attr, attr_type in instance.openapi_types.items():
            if self.value is not None \
                    and instance.attribute_map[attr] in self.value \
                    and isinstance(self.value, (list, dict)):
                value = self.value[instance.attribute_map[attr]]
                setattr(instance, attr, Data(value).deserialize(attr_type))
        return instance

    def deserialize_list(self, boxed_type: Type) -> List:
        """Deserialize a list and its elements.
        :param boxed_type: class literal.
        :type boxed_type: Type
        :return: deserialized list
        :rtype: List
        """
        return [Data(data).deserialize(boxed_type) for data in self.value]

    def deserialize_dict(self, boxed_type: Type) -> Dict:
        """Deserialize a dict and its elements.
        :param boxed_type: class literal.
        :type boxed_type: Type
        :return: deserialized dict.
        :rtype: Dict
        """
        return {k: Data(v).deserialize(boxed_type) for k, v in self.value.items()}
