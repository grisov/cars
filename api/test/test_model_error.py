import unittest
from api.models.error import Error


class TestErrorModel(unittest.TestCase):
    """Test case for testing the Error model."""

    def test_attributes(self):
        """Testing the attributes of the data model."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        self.assertIsInstance(error.status, int)
        self.assertEqual(error.status, 404)
        self.assertIsInstance(error.title, str)
        self.assertEqual(error.title, "Not Found")
        self.assertIsInstance(error.detail, str)
        self.assertEqual(error.detail, "The requested URL was not found on the server.")
        self.assertIsInstance(error.type, str)
        self.assertEqual(error.type, "about:blank")

    def test_required_status(self):
        """Testing the required attribute of the data model."""
        error = Error(
            status=500,
            title="Internal Server Error",
            detail="The server encountered an internal error.",
            type="about:blank"
        )
        error.status=0
        self.assertEqual(error.status, 0)
        error.status=-123
        self.assertEqual(error.status, -123)
        with self.assertRaises(ValueError):
            error.status=None
        self.assertIsNotNone(error.status)
        self.assertIsInstance(error.status, int)

    def test_required_title(self):
        """Testing the required attribute of the data model."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The requested URL was not found on the server.",
            type="about:blank"
        )
        error.title="Internal Server Error"
        self.assertEqual(error.title, "Internal Server Error")
        error.title=''
        self.assertEqual(error.title, "")
        with self.assertRaises(ValueError):
            error.title=None
        self.assertIsNotNone(error.title)
        self.assertIsInstance(error.title, str)

    def test_openapi_types(self):
        """Testing declared attribute types."""
        error = Error(
            status=200,
            title="Success",
            detail="Successful request",
            type="about:blank"
        )
        self.assertTrue(hasattr(error, "openapi_types"))
        self.assertIsInstance(error.openapi_types, dict)
        self.assertEqual(len(error.openapi_types), 4)
        self.assertIn("status", error.openapi_types)
        self.assertIn("title", error.openapi_types)
        self.assertIn("detail", error.openapi_types)
        self.assertIn("type", error.openapi_types)
        self.assertEqual(error.openapi_types["status"], int)
        self.assertEqual(error.openapi_types["title"], str)
        self.assertEqual(error.openapi_types["detail"], str)
        self.assertEqual(error.openapi_types["type"], str)

    def test_attribute_map(self):
        """Testing declared attribute names."""
        error = Error(
            status=500,
            title="Internal Server Error",
            detail="The server encountered an internal error.",
            type="about:blank"
        )
        self.assertTrue(hasattr(error, "attribute_map"))
        self.assertIsInstance(error.attribute_map, dict)
        self.assertEqual(len(error.attribute_map), 4)
        self.assertIn("status", error.attribute_map)
        self.assertIn("title", error.attribute_map)
        self.assertIn("detail", error.attribute_map)
        self.assertIn("type", error.attribute_map)
        self.assertEqual(error.attribute_map["status"], 'status')
        self.assertEqual(error.attribute_map["title"], 'title')
        self.assertEqual(error.attribute_map["detail"], 'detail')
        self.assertEqual(error.attribute_map["type"], 'type')

    def test_from_to_dict(self):
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "status": 500,
            "title": "Internal Server Error",
            "detail": "The server encountered an internal error.",
            "type": "about:blank"
        }
        error = Error.from_dict(data)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.status, 500)
        self.assertEqual(error.title, "Internal Server Error")
        self.assertEqual(error.detail, "The server encountered an internal error.")
        self.assertEqual(error.type, "about:blank")
        info = error.to_dict()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['status'], 500)
        self.assertEqual(info['title'], "Internal Server Error")
        self.assertEqual(info['detail'], "The server encountered an internal error.")
        self.assertEqual(info['type'], "about:blank")

    def test_to_str(self):
        """Testing the method of converting the model to a string."""
        error = Error(
            status=404,
            title="Not Found",
            detail="The URL not found",
            type="about:blank"
        )
        line = "{'status': 404, 'title': 'Not Found', 'detail': 'The URL not found', 'type': 'about:blank'}"
        self.assertIsInstance(error, Error)
        self.assertIsInstance(line, str)
        self.assertEqual(error.to_str(), line)
        self.assertEqual(error.__repr__(), line)
        self.assertEqual(str(error), line)

    def test_eq_models(self):
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
        self.assertEqual(error1.status, error2.status)
        self.assertEqual(error1.title, error2.title)
        self.assertEqual(error1.detail, error2.detail)
        self.assertEqual(error1.type, error2.type)
        self.assertTrue(error1 == error2)
        self.assertTrue(error1.__eq__(error2))

    def test_ne_models(self):
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
        self.assertNotEqual(error1.status, error2.status)
        self.assertNotEqual(error1.title, error2.title)
        self.assertNotEqual(error1.detail, error2.detail)
        self.assertEqual(error1.type, error2.type)
        self.assertFalse(error1 == error2)
        self.assertTrue(error1 != error2)
        self.assertTrue(error1.__ne__(error2))
        self.assertTrue(error2.__ne__(error1))

    def test_none_values(self):
        """Testing the data model with None values."""
        error = Error(
            status=503,
            title="Service Unavailable"
        )
        self.assertIsNotNone(error.status)
        self.assertIsNotNone(error.title)
        self.assertIsNone(error.detail)
        self.assertIsNone(error.type)


if __name__ == '__main__':
    unittest.main()
