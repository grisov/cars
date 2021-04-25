import unittest
from api.models.error import Error


class TestErrorModel(unittest.TestCase):
    """Test case for testing the Error model."""

    def test_attributes(self) -> None:
        """Testing the attributes of the data model."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        self.assertIsInstance(error.status, int,
            "Check the data type of the model property")
        self.assertEqual(error.status, 404,
            f"The status of the error is `{error.status}`")
        self.assertIsInstance(error.title, str,
            "Check the data type of the model property")
        self.assertEqual(error.title, "Not Found",
            f"The title of the error is `{error.title}`")
        self.assertIsInstance(error.detail, str,
            "Check the data type of the model property")
        self.assertEqual(error.detail, "The requested URL was not found on the server.",
            f"The detail of the error is `{error.detail}`")
        self.assertIsInstance(error.type, str,
            "Check the data type of the model property")
        self.assertEqual(error.type, "about:blank",
            f"The type of the error is `{error.type}`")

    def test_required_status(self) -> None:
        """Testing the required attribute 'status' of the data model."""
        error = Error(
            status=500,
            title="Internal Server Error",
            detail="The server encountered an internal error.",
            type="about:blank"
        )
        error.status = 0
        self.assertEqual(error.status, 0,
            f"The new status of the error is `{error.status}`")
        error.status = -123
        self.assertEqual(error.status, -123,
            f"The new status of the error is `{error.status}`")
        with self.assertRaises(ValueError):
            error.status = None  # None is not allowed
        self.assertIsNotNone(error.status,
            "The status of the error still contains the not empty value")
        self.assertIsInstance(error.status, int,
            "Check the data type of the model property")

    def test_required_title(self) -> None:
        """Testing the required attribute 'title' of the data model."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        error.title = "Internal Server Error"
        self.assertEqual(error.title, "Internal Server Error",
            f"The new title of the error is `{error.title}`")
        error.title = ''
        self.assertEqual(error.title, "",
            f"The new title of the error is `{error.title}`")
        with self.assertRaises(ValueError):
            error.title = None  # None is not allowed
        self.assertIsNotNone(error.title,
            "The title of the error still contains the not empty value")
        self.assertIsInstance(error.title, str,
            "Check the data type of the model property")

    def test_openapi_types(self) -> None:
        """Testing declared attribute types."""
        error = Error(
            status=200,
            title="Success",
            detail="Successful request",
            type="about:blank"
        )
        self.assertTrue(hasattr(error, "openapi_types"),
            "The model contains the `openapi_types` attribute")
        self.assertIsInstance(error.openapi_types, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(error.openapi_types), 4,
            f"The length of the openapi_types dict is {len(error.openapi_types)}")
        self.assertIn("status", error.openapi_types,
            "The `status` key is present in the openapi_types dict")
        self.assertIn("title", error.openapi_types,
            "The `title` key is present in the openapi_types dict")
        self.assertIn("detail", error.openapi_types,
            "The `detail` key is present in the openapi_types dict")
        self.assertIn("type", error.openapi_types,
            "The `type` key is present in the openapi_types dict")
        self.assertEqual(error.openapi_types["status"], int,
            "Check the value in the openapi_types dict")
        self.assertEqual(error.openapi_types["title"], str,
            "Check the value in the openapi_types dict")
        self.assertEqual(error.openapi_types["detail"], str,
            "Check the value in the openapi_types dict")
        self.assertEqual(error.openapi_types["type"], str,
            "Check the value in the openapi_types dict")

    def test_attribute_map(self) -> None:
        """Testing declared attribute names."""
        error = Error(
            status=500,
            title="Internal Server Error",
            detail="The server encountered an internal error.",
            type="about:blank"
        )
        self.assertTrue(hasattr(error, "attribute_map"),
            "The model contains the `attribute_map` attribute")
        self.assertIsInstance(error.attribute_map, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(error.attribute_map), 4,
            f"The length of the attribute_map dict is {len(error.attribute_map)}")
        self.assertIn("status", error.attribute_map,
            "The `status` key is present in the attribute_map dict")
        self.assertIn("title", error.attribute_map,
            "The `title` key is present in the attribute_map dict")
        self.assertIn("detail", error.attribute_map,
            "The `detail` key is present in the attribute_map dict")
        self.assertIn("type", error.attribute_map,
            "The `type` key is present in the attribute_map dict")
        self.assertEqual(error.attribute_map["status"], 'status',
            f"Under the `status` key there is a value of `{error.attribute_map['status']}`")
        self.assertEqual(error.attribute_map["title"], 'title',
            f"Under the `title` key there is a value of `{error.attribute_map['title']}`")
        self.assertEqual(error.attribute_map["detail"], 'detail',
            f"Under the `detail` key there is a value of `{error.attribute_map['detail']}`")
        self.assertEqual(error.attribute_map["type"], 'type',
            f"Under the `type` key there is a value of `{error.attribute_map['type']}`")

    def test_from_to_dict(self) -> None:
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "status": 500,
            "title": "Internal Server Error",
            "detail": "The server encountered an internal error.",
            "type": "about:blank"
        }
        error = Error.from_dict(data)
        self.assertIsInstance(error, Error,
            "Check the type of the variable")
        self.assertEqual(error.status, 500,
            f"The `status` property contains a value of `{error.status}`")
        self.assertEqual(error.title, "Internal Server Error",
            f"The `title` property contains a value of `{error.title}`")
        self.assertEqual(error.detail, "The server encountered an internal error.",
            f"The `detail` property contains a value of `{error.detail}`")
        self.assertEqual(error.type, "about:blank",
            f"The `type` property contains a value of `{error.type}`")
        info = error.to_dict()
        self.assertIsInstance(info, dict,
            "Check the type of the variable")
        self.assertEqual(info['status'], 500,
            f"The `status` key contains a value of `{info['status']}`")
        self.assertEqual(info['title'], "Internal Server Error",
            f"The `title` key contains a value of `{info['title']}`")
        self.assertEqual(info['detail'], "The server encountered an internal error.",
            f"The `detail` key contains a value of `{info['detail']}`")
        self.assertEqual(info['type'], "about:blank",
            f"The `type` key contains a value of `{info['type']}`")

    def test_to_str(self) -> None:
        """Testing the method of converting the model to a string."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The URL not found",
            type="about:blank"
        )
        line = "{'status': 404, 'title': 'Not Found', 'detail': 'The URL not found', 'type': 'about:blank'}"
        self.assertIsInstance(error, Error,
            "Check the data type of the variable")
        self.assertIsInstance(line, str,
            "Check the data type of the variable")
        self.assertEqual(error.to_str(), line,
            f"The to_str() method returns the following value: `{error.to_str()}`")
        self.assertEqual(error.__repr__(), line,
            f"The __repr__() method returns the following value: `{error.__repr__()}`")
        self.assertEqual(str(error), line,
            f"Convert to a string returns the following value: `{str(error)}`")

    def test_eq_models(self) -> None:
        """Testing to check models for equality."""
        error1 = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        error2 = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        self.assertEqual(error1.status, error2.status,
            f"The `status` property has a value of `{error1.status}`")
        self.assertEqual(error1.title, error2.title,
            f"The `title` property has a value of `{error1.title}`")
        self.assertEqual(error1.detail, error2.detail,
            f"The `detail` property has a value of `{error1.detail}`")
        self.assertEqual(error1.type, error2.type,
            f"The `type` property has a value of `{error1.type}`")
        self.assertTrue(error1 == error2,
            "Both objects are the same")
        self.assertTrue(error1.__eq__(error2),
            f"The equality comparison function returns {str(error1.__eq__(error2))}")

    def test_ne_models(self) -> None:
        """Testing to check models for inequality."""
        error1 = Error(
            status=500,
            title="Internal Server Error",
            detail="The server encountered an internal error.",
            type="about:blank"
        )
        error2 = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        self.assertNotEqual(error1.status, error2.status,
            "The `status` properties have the differ values")
        self.assertNotEqual(error1.title, error2.title,
            "The `title` properties have the differ values")
        self.assertNotEqual(error1.detail, error2.detail,
            "The `detail` properties have the differ values")
        self.assertEqual(error1.type, error2.type,
            "The `type` properties have the same values")
        self.assertFalse(error1 == error2,
            "Objects are different")
        self.assertTrue(error1 != error2,
            "Objects are not equal")
        self.assertTrue(error1.__ne__(error2),
            f"The inequality comparison function returns {str(error1.__ne__(error2))}")
        self.assertTrue(error2.__ne__(error1),
            f"The inequality comparison function returns {str(error2.__ne__(error1))}")

    def test_none_values(self) -> None:
        """Testing the data model with None values."""
        error = Error(
            status=503,
            title="Service Unavailable"
        )
        self.assertIsNotNone(error.status,
            "The value of the `status` property is not empty")
        self.assertEqual(error.status, 503,
            f"The `status` property has a value of `{error.status}`")
        self.assertIsNotNone(error.title,
            "The value of the `title` property is not empty")
        self.assertEqual(error.title, "Service Unavailable",
            f"The `title` property has a value of `{error.title}`")
        self.assertIsNone(error.detail,
            "The `detail` property has an empty value")
        self.assertIsNotNone(error.type,
            "The value of the `type` property is not empty")
        self.assertEqual(error.type, "about:blank",
            f"The `type` property has a value of `{error.type}`")


if __name__ == '__main__':
    unittest.main()
