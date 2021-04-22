from typing import List, Dict, Optional
from api.models.base_model import Model


class Error(Model):
    """Representation of the data structure for the error."""

    def __init__(
            self,
            status: Optional[int]=None,
            title: Optional[str]=None,
            detail: Optional[str]=None,
            type: Optional[str]=None
        ) -> None:
        """Error model defined in OpenAPI specification.
        :param status: The status code of this error
        :type status: Optional[int]
        :param title: The title of this error
        :type title: Optional[str]
        :param detail: The detailed information about this error
        :type detail: Optional[str]
        :param type: The type of this error
        :type type: Optional[str]
        """
        self.openapi_types = {
            'status': int,
            'title': str,
            'detail': str,
            'type': str
        }
        self.attribute_map = {
            'status': 'status',
            'title': 'title',
            'detail': 'detail',
            'type': 'type'
        }
        self._status = status
        self._title = title
        self._detail = detail
        self._type = type

    @property
    def status(self) -> Optional[int]:
        """Get the status of this error.
        :return: The error code, usually HTTP status code
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status: Optional[int]) -> None:
        """Set the status code of this error.
        :param status: The error code, usually HTTP status
        :type status: Optional[int]
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")
        self._status = status

    @property
    def title(self) -> Optional[str]:
        """Get the common title of the error.
        :return: The title of this error
        :rtype: Optional[str]
        """
        return self._title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        """Set the common title of the error.
        :param title: The title of this error
        :type title: Optional[str]
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")
        self._title = title

    @property
    def detail(self) -> Optional[str]:
        """Get the detailed description of the error.
        :return: The detailed description of the error
        :rtype: Optional[str]
        """
        return self._detail

    @detail.setter
    def detail(self, detail: Optional[str]) -> None:
        """Set the detailed description of the error.
        :param detail: The detailed description of the error
        :type detail: Optional[str]
        """
        self._detail = detail

    @property
    def type(self) -> str:
        """Get the type of the error.
        :return: The error type
        :rtype: str
        """
        return self._type or "about:blank"

    @type.setter
    def type(self, type: Optional[str]) -> None:
        """Set the information about the type of the error.
        :param type: The type of the error
        :type type: Optional[str]
        """
        self._type = type
