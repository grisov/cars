import unittest
from datetime import date
from api.models.course import Course
from api.utils import Data


class TestCourseModel(unittest.TestCase):
    """Test case for testing the Course model."""

    def test_attributes(self):
        """Testing the attributes of the data model."""
        course = Course(
            name="Technology",
            start="2021-04-28",
            end="2021-05-15",
            amount=15,
            id=-1
        )
        self.assertIsInstance(course.name, str)
        self.assertEqual(course.name, "Technology")

        self.assertIsInstance(course.start, date)
        self.assertEqual(course.start.isoformat(), "2021-04-28")
        course.start = Data("2021-04-28").deserialize(date)
        self.assertIsInstance(course.start, date)
        self.assertEqual(course.start.year, 2021)
        self.assertEqual(course.start.month, 4)
        self.assertEqual(course.start.day, 28)

        self.assertIsInstance(course.end, date)
        self.assertEqual(course.end.isoformat(), "2021-05-15")
        course.end = Data("2021-07-17").deserialize(date)
        self.assertIsInstance(course.end, date)
        self.assertEqual(course.end.year, 2021)
        self.assertEqual(course.end.month, 7)
        self.assertEqual(course.end.day, 17)

    def test_required_name(self):
        """Testing the required attribute of the data model."""
        course = Course(
            name="test",
            start="2000-01-01",
            end="2099-12-31",
            amount=1
        )
        course.name="Python for beginners"
        self.assertEqual(course.name, 'Python for beginners')
        with self.assertRaises(ValueError):
            course.name=None
        self.assertIsNotNone(course.name)
        course.name="ukr"
        self.assertEqual(course.name, 'ukr')
        with self.assertRaises(ValueError):
            course.name='x'
        with self.assertRaises(ValueError):
            course.name=''
        self.assertIsNotNone(course.name)
        self.assertIsInstance(course.name, (str))
        self.assertNotEqual(course.name, '')

    def test_required_start_end(self):
        """Testing the required attributes of the data model."""
        course = Course(
            name="Python is awesome!",
            start=Data("2000-01-01").deserialize(date),
            end=Data("2029-12-31").deserialize(date),
            amount=100
        )
        self.assertIsInstance(course.start, date)
        self.assertEqual(course.start.year, 2000)
        self.assertEqual(course.start.month, 1)
        self.assertEqual(course.start.day, 1)
        with self.assertRaises(ValueError):
            course.start=None
        self.assertIsNotNone(course.start)
        self.assertEqual(course.start.isoformat(), "2000-01-01")

        self.assertIsInstance(course.end, date)
        self.assertEqual(course.end.year, 2029)
        self.assertEqual(course.end.month, 12)
        self.assertEqual(course.end.day, 31)
        with self.assertRaises(ValueError):
            course.end=None
        self.assertIsNotNone(course.end)
        self.assertEqual(course.end.isoformat(), "2029-12-31")

    def test_comparison_start_end(self):
        """Testing the comparison of start and end dates."""
        course = Course()
        course.start = "2020-08-17"
        course.end = "2020-08-17"
        course.end = "2020-08-18"
        with self.assertRaises(ValueError):
            course.end = "2020-08-16"
            course.end = "2020-07-18"
            course.end = "2019-08-18"

        course.start = Data("2020-08-17").deserialize(date)
        course.end = Data("2020-08-17").deserialize(date)
        course.end = Data("2020-08-18").deserialize(date)
        with self.assertRaises(ValueError):
            course.end = Data("2020-08-16").deserialize(date)
            course.end = Data("2020-07-18").deserialize(date)
            course.end = Data("2019-08-18").deserialize(date)

    def test_required_amount(self):
        """Testing the required attribute of the data model."""
        course = Course(
            name="Python is awesome!",
            start=Data("2000-01-01").deserialize(date),
            end=Data("2029-12-31").deserialize(date),
            amount=100
        )
        self.assertEqual(course.amount, 100)
        with self.assertRaises(ValueError):
            course.amount=None
        course.amount=1
        self.assertEqual(course.amount, 1)
        course.amount=255
        self.assertEqual(course.amount, 255)
        with self.assertRaises(ValueError):
            course.amount=0
            course.amount=-1
            course.amount=256

    def test_openapi_types(self):
        """Testing declared attribute types."""
        course = Course(
            name="Python is awesome!",
            start=Data("2029-09-29").deserialize(date),
            end=Data("2037-07-27").deserialize(date),
            amount=255
        )
        self.assertTrue(hasattr(course, "openapi_types"))
        self.assertIsInstance(course.openapi_types, dict)
        self.assertEqual(len(course.openapi_types), 5)
        self.assertIn("name", course.openapi_types)
        self.assertIn("start", course.openapi_types)
        self.assertIn("end", course.openapi_types)
        self.assertIn("amount", course.openapi_types)
        self.assertIn("id", course.openapi_types)
        self.assertEqual(course.openapi_types["name"], str)
        self.assertEqual(course.openapi_types["start"], date)
        self.assertEqual(course.openapi_types["end"], date)
        self.assertEqual(course.openapi_types["amount"], int)
        self.assertEqual(course.openapi_types["id"], int)

    def test_attribute_map(self):
        """Testing declared attribute names."""
        course = Course(
            name="Python is awesome!",
            start=Data("2029-09-29").deserialize(date),
            end=Data("2037-07-27").deserialize(date),
            amount=255
        )
        self.assertTrue(hasattr(course, "attribute_map"))
        self.assertIsInstance(course.attribute_map, dict)
        self.assertEqual(len(course.attribute_map), 5)
        self.assertIn("name", course.attribute_map)
        self.assertIn("start", course.attribute_map)
        self.assertIn("end", course.attribute_map)
        self.assertIn("amount", course.attribute_map)
        self.assertIn("id", course.attribute_map)
        self.assertEqual(course.attribute_map["name"], 'name')
        self.assertEqual(course.attribute_map["start"], 'start')
        self.assertEqual(course.attribute_map["end"], 'end')
        self.assertEqual(course.attribute_map["amount"], 'amount')
        self.assertEqual(course.attribute_map["id"], 'id')

    def test_from_to_dict(self):
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "name": "Quality Assurance",
            "start": Data("2021-05-07").deserialize(date),
            "end": Data("2021-11-29").deserialize(date),
            "amount": 123,
            "id": 7
        }
        course = Course.from_dict(data)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.name, 'Quality Assurance')
        self.assertEqual(course.start, data['start'])
        self.assertEqual(course.end, data['end'])
        self.assertEqual(course.amount, data['amount'])
        self.assertEqual(course.id, data['id'])
        info = course.to_dict()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['name'], 'Quality Assurance')
        self.assertEqual(info['start'], data['start'])
        self.assertEqual(info['end'], data['end'])
        self.assertEqual(info['amount'], 123)
        self.assertEqual(info['id'], 7)
        self.assertEqual(info, data)

    def test_to_str(self):
        """Testing the method of converting the model to a string."""
        course = Course(
            name="Quality",
            start="2021-05-07",
            end="2021-11-29",
            amount=17,
            id=5
        )
        line = "{'name': 'Quality', 'start': '2021-05-07', 'end': '2021-11-29', 'amount': 17, 'id': 5}"
        self.assertIsInstance(course, Course)
        self.assertIsInstance(line, str)
        self.assertEqual(course.to_str(), line)
        self.assertEqual(course.__repr__(), line)
        self.assertEqual(str(course), line)

    def test_eq_models(self):
        """Testing to check models for equality."""
        course1 = Course(
            name="Python is awesome!",
            start=Data("2021-09-03").deserialize(date),
            end=Data("2021-12-23").deserialize(date),
            amount=39,
            id=97
        )
        course2 = Course(
            name="Python is awesome!",
            start=Data("2021-09-03").deserialize(date),
            end=Data("2021-12-23").deserialize(date),
            amount=39,
            id=97
        )
        self.assertEqual(course1.name, course2.name)
        self.assertEqual(course1.start, course2.start)
        self.assertEqual(course1.end, course2.end)
        self.assertEqual(course1.amount, course2.amount)
        self.assertEqual(course1.id, course2.id)
        self.assertTrue(course1 == course2)
        self.assertTrue(course1.__eq__(course2))

    def test_ne_models(self):
        """Testing to check models for inequality."""
        course1 = Course(
            name="OpenAPI/Swagger",
            start=Data("2021-07-11").deserialize(date),
            end=Data("2021-12-23").deserialize(date),
            amount=39,
            id=96
        )
        course2 = Course(
            name="Python is awesome!",
            start=Data("2021-02-07").deserialize(date),
            end=Data("2021-07-11").deserialize(date),
            amount=39,
            id=97
        )
        self.assertNotEqual(course1.name, course2.name)
        self.assertNotEqual(course1.start, course2.start)
        self.assertNotEqual(course1.end, course2.end)
        self.assertEqual(course1.amount, course2.amount)
        self.assertNotEqual(course1.id, course2.id)
        self.assertFalse(course1 == course2)
        self.assertTrue(course1 != course2)
        self.assertTrue(course1.__ne__(course2))
        self.assertTrue(course2.__ne__(course1))

    def test_default_values(self):
        """Testing the data model with default null values."""
        course = Course()
        self.assertEqual(course.name, '--')
        self.assertIsNotNone(course.start)
        self.assertEqual(course.start.isoformat(), "1970-01-01")
        self.assertIsNotNone(course.end)
        self.assertEqual(course.end.isoformat(), "1970-01-01")
        self.assertEqual(course.amount, 1)
        self.assertEqual(course.id, -1)


if __name__ == '__main__':
    unittest.main()
