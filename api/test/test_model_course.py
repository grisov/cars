import unittest
from datetime import date
from api.models.course import Course
from api.utils import Data


class TestCourseModel(unittest.TestCase):
    """Test case for testing the Course model."""

    def test_attributes(self) -> None:
        """Testing the attributes of the data model."""
        course = Course(
            name="Technology",
            start="2021-04-28",
            end="2021-05-15",
            amount=15,
            id=-1
        )
        self.assertIsInstance(course.name, str,
            "Check the data type of the model property")
        self.assertEqual(course.name, "Technology",
            f"The name of the course is `{course.name}`")
        self.assertIsInstance(course.start, date,
            "Check the data type of the model property")
        self.assertEqual(course.start.isoformat(), "2021-04-28",
            f"The course starting date is `{course.start.isoformat()}`")
        course.start = Data("2021-04-28").deserialize(date)
        self.assertIsInstance(course.start, date,
            "Check the data type of the model property")
        self.assertEqual(course.start.year, 2021,

            f"The year of the beginning of the course is {course.start.year}")
        self.assertEqual(course.start.month, 4,
            f"The month of the beginning of the course is {course.start.month}")
        self.assertEqual(course.start.day, 28,
            f"The day of the beginning of the course is {course.start.day}")

        self.assertIsInstance(course.end, date,
            "Check the data type of the model property")
        self.assertEqual(course.end.isoformat(), "2021-05-15",
            f"The course ending date is `{course.end.isoformat()}`")
        course.end = Data("2021-07-17").deserialize(date)
        self.assertIsInstance(course.end, date,
            "Check the data type of the model property")
        self.assertEqual(course.end.year, 2021,
            f"The year of the gratuation of the course is {course.end.year}")
        self.assertEqual(course.end.month, 7,
            f"The month of the gratuation of the course is {course.end.month}")
        self.assertEqual(course.end.day, 17,
            f"The day of the gratuation of the course is {course.end.day}")

    def test_required_name(self) -> None:
        """Testing the required attribute 'name' of the data model."""
        course = Course(
            name="test",
            start="2000-01-01",
            end="2099-12-31",
            amount=1
        )
        course.name="Python for beginners"
        self.assertEqual(course.name, 'Python for beginners',
            f"The new name of the course is `{course.name}`")
        with self.assertRaises(ValueError):
            course.name=None  # None is not allowed
        self.assertIsNotNone(course.name,
            "The name of the course still contains the not empty value")
        course.name="ukr"
        self.assertEqual(course.name, 'ukr',
            f"The new name of the course is `{course.name}`")
        with self.assertRaises(ValueError):
            course.name='x'  # less than 2 characters
            course.name=''  # empty string
        self.assertIsNotNone(course.name,
            "The name of the course still contains the not empty value")
        self.assertIsInstance(course.name, (str),
            "Check the data type of the model property")
        self.assertNotEqual(course.name, '',
            "The name of the course is not an empty string")

    def test_required_start_end(self) -> None:
        """Testing the required attributes 'start' and 'end' of the data model."""
        course = Course(
            name="Python is awesome!",
            start=Data("2000-01-01").deserialize(date),
            end=Data("2029-12-31").deserialize(date),
            amount=100
        )
        self.assertIsInstance(course.start, date,
            "Check the data type of the model property")
        self.assertEqual(course.start.year, 2000,
            f"The year of the beginning of the course is {course.start.year}")
        self.assertEqual(course.start.month, 1,
            f"The month of the beginning of the course is {course.start.month}")
        self.assertEqual(course.start.day, 1,
            f"The day of the beginning of the course is {course.start.day}")
        with self.assertRaises(ValueError):
            course.start=None  # None is not allowed
        self.assertIsNotNone(course.start,
            "The starting date of the course still contains the not empty value")
        self.assertEqual(course.start.isoformat(), "2000-01-01",
            f"The course starting date is `{course.start.isoformat()}`")

        self.assertIsInstance(course.end, date,
            "Check the data type of the model property")
        self.assertEqual(course.end.year, 2029,
            f"The year of the gratuation of the course is {course.end.year}")
        self.assertEqual(course.end.month, 12,
            f"The month of the gratuation of the course is {course.end.month}")
        self.assertEqual(course.end.day, 31,
            f"The day of the gratuation of the course is {course.end.day}")
        with self.assertRaises(ValueError):
            course.end=None  # None is not allowed
        self.assertIsNotNone(course.end,
            "The gratuation date of the course still contains the not empty value")
        self.assertEqual(course.end.isoformat(), "2029-12-31",
            f"The course gratuation date is `{course.end.isoformat()}`")

    def test_comparison_start_end(self) -> None:
        """Testing the comparison of start and end dates."""
        course = Course()
        course.start = "2020-08-17"
        course.end = "2020-08-17"  # start == end
        course.end = "2020-08-18"  # 18 > 17
        with self.assertRaises(ValueError):
            course.end = "2020-08-16"  # 16 < 17
            course.end = "2020-07-18"  # 7 < 8
            course.end = "2019-08-18"  # 2019 < 2020

        course.start = Data("2020-08-17").deserialize(date)
        course.end = Data("2020-08-17").deserialize(date)  # start == end
        course.end = Data("2020-08-18").deserialize(date)  # 18 > 17
        with self.assertRaises(ValueError):
            course.end = Data("2020-08-16").deserialize(date)  # 16 < 17
            course.end = Data("2020-07-18").deserialize(date)  # 7 < 8
            course.end = Data("2019-08-18").deserialize(date)  # 2019 < 2020

    def test_required_amount(self) -> None:
        """Testing the required attribute 'amount' of the data model."""
        course = Course(
            name="Python is awesome!",
            start=Data("2000-01-01").deserialize(date),
            end=Data("2029-12-31").deserialize(date),
            amount=100
        )
        self.assertEqual(course.amount, 100,
            f"The number of course lectures is `{course.amount}`")
        with self.assertRaises(ValueError):
            course.amount=None  # None is not allowed
        course.amount=1
        self.assertEqual(course.amount, 1,
            f"The number of course lectures is `{course.amount}`")
        course.amount=255
        self.assertEqual(course.amount, 255,
            f"The number of course lectures is `{course.amount}`")
        with self.assertRaises(ValueError):
            course.amount=0  # 0 < 1
            course.amount=-1  # -1 < 1
            course.amount=256  # 256 > 255

    def test_openapi_types(self) -> None:
        """Testing declared attribute types."""
        course = Course(
            name="Python is awesome!",
            start=Data("2029-09-29").deserialize(date),
            end=Data("2037-07-27").deserialize(date),
            amount=255
        )
        self.assertTrue(hasattr(course, "openapi_types"),
            "The model contains the `openapi_types` attribute")
        self.assertIsInstance(course.openapi_types, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(course.openapi_types), 5,
            f"The length of the openapi_types dict is {len(course.openapi_types)}")
        self.assertIn("name", course.openapi_types,
            "The `name` key is present in the openapi_types dict")
        self.assertIn("start", course.openapi_types,
            "The `start` key is present in the openapi_types dict")
        self.assertIn("end", course.openapi_types,
            "The `end` key is present in the openapi_types dict")
        self.assertIn("amount", course.openapi_types,
            "The `amount` key is present in the openapi_types dict")
        self.assertIn("id", course.openapi_types,
            "The `id` key is present in the openapi_types dict")
        self.assertEqual(course.openapi_types["name"], str,
            "Check the value in the openapi_types dict")
        self.assertEqual(course.openapi_types["start"], date,
            "Check the value in the openapi_types dict")
        self.assertEqual(course.openapi_types["end"], date,
            "Check the value in the openapi_types dict")
        self.assertEqual(course.openapi_types["amount"], int,
            "Check the value in the openapi_types dict")
        self.assertEqual(course.openapi_types["id"], int,
            "Check the value in the openapi_types dict")

    def test_attribute_map(self) -> None:
        """Testing declared attribute names."""
        course = Course(
            name="Python is awesome!",
            start=Data("2029-09-29").deserialize(date),
            end=Data("2037-07-27").deserialize(date),
            amount=255
        )
        self.assertTrue(hasattr(course, "attribute_map"),
            "The model contains the `attribute_map` attribute")
        self.assertIsInstance(course.attribute_map, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(course.attribute_map), 5,
            f"The length of the attribute_map dict is {len(course.attribute_map)}")
        self.assertIn("name", course.attribute_map,
            "The `name` key is present in the attribute_map dict")
        self.assertIn("start", course.attribute_map,
            "The `start` key is present in the attribute_map dict")
        self.assertIn("end", course.attribute_map,
            "The `end` key is present in the attribute_map dict")
        self.assertIn("amount", course.attribute_map,
            "The `amount` key is present in the attribute_map dict")
        self.assertIn("id", course.attribute_map,
            "The `id` key is present in the attribute_map dict")
        self.assertEqual(course.attribute_map["name"], 'name',
            f"Under the `name` key there is a value of `{course.attribute_map['name']}`")
        self.assertEqual(course.attribute_map["start"], 'start',
            f"Under the `start` key there is a value of `{course.attribute_map['start']}`")
        self.assertEqual(course.attribute_map["end"], 'end',
            f"Under the `end` key there is a value of `{course.attribute_map['end']}`")
        self.assertEqual(course.attribute_map["amount"], 'amount',
            f"Under the `amount` key there is a value of `{course.attribute_map['amount']}`")
        self.assertEqual(course.attribute_map["id"], 'id',
            f"Under the `id` key there is a value of `{course.attribute_map['id']}`")

    def test_from_to_dict(self) -> None:
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "name": "Quality Assurance",
            "start": Data("2021-05-07").deserialize(date),
            "end": Data("2021-11-29").deserialize(date),
            "amount": 123,
            "id": 7
        }
        course = Course.from_dict(data)
        self.assertIsInstance(course, Course,
            "Check the type of the variable")
        self.assertEqual(course.name, 'Quality Assurance',
            f"The `name` property contains a value of `{course.name}`")
        self.assertEqual(course.start, data['start'],
            f"The `start` property contains a value of `{course.start.isoformat()}`")
        self.assertEqual(course.end, data['end'],
            f"The `end` property contains a value of `{course.end.isoformat()}`")
        self.assertEqual(course.amount, data['amount'],
            f"The `amount` property contains a value of `{course.amount}`")
        self.assertEqual(course.id, data['id'],
            f"The `id` property contains a value of `{course.id}`")
        info = course.to_dict()
        self.assertIsInstance(info, dict,
            "Check the type of the variable")
        self.assertEqual(info['name'], 'Quality Assurance',
            f"The `name` key contains a value of `{info['name']}`")
        self.assertEqual(info['start'], data['start'],
            f"The `start` key contains a value of `{info['start'].isoformat()}`")
        self.assertEqual(info['end'], data['end'],
            f"The `end` key contains a value of `{info['end'].isoformat()}`")
        self.assertEqual(info['amount'], 123,
            f"The `amount` key contains a value of `{info['amount']}`")
        self.assertEqual(info['id'], 7,
            f"The `id` key contains a value of `{info['id']}`")
        self.assertEqual(info, data,
            "The converted dict is identical to the original")

    def test_to_str(self) -> None:
        """Testing the method of converting the model to a string."""
        course = Course(
            name="Quality",
            start="2021-05-07",
            end="2021-11-29",
            amount=17,
            id=5
        )
        line = "{'name': 'Quality', 'start': '2021-05-07', 'end': '2021-11-29', 'amount': 17, 'id': 5}"
        self.assertIsInstance(course, Course,
            "Check the data type of the variable")
        self.assertIsInstance(line, str,
            "Check the data type of the variable")
        self.assertEqual(course.to_str(), line,
            f"The to_str() method returns the following value: `{course.to_str()}`")
        self.assertEqual(course.__repr__(), line,
            f"The __repr__() method returns the following value: `{course.__repr__()}`")
        self.assertEqual(str(course), line,
            f"Convert to a string returns the following value: `{str(course)}`")

    def test_eq_models(self) -> None:
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
        self.assertEqual(course1.name, course2.name,
            "The `name` properties have the same values")
        self.assertEqual(course1.start, course2.start,
            "The `start` properties have the same values")
        self.assertEqual(course1.end, course2.end,
            "The `end` properties have the same values")
        self.assertEqual(course1.amount, course2.amount,
            "The `amount` properties have the same values")
        self.assertEqual(course1.id, course2.id,
            "The `id` properties have the same values")
        self.assertTrue(course1 == course2,
            "Both objects are the same")
        self.assertTrue(course1.__eq__(course2),
            "The equality comparison function returns True")

    def test_ne_models(self) -> None:
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
        self.assertNotEqual(course1.name, course2.name,
            "The `name` properties have the differ values")
        self.assertNotEqual(course1.start, course2.start,
            "The `start` properties have the differ values")
        self.assertNotEqual(course1.end, course2.end,
            "The `end` properties have the differ values")
        self.assertEqual(course1.amount, course2.amount,
            "The `amount` properties have the same values")
        self.assertNotEqual(course1.id, course2.id,
            "The `id` properties have the differ values")
        self.assertFalse(course1 == course2,
            "Objects are different")
        self.assertTrue(course1 != course2,
            "Objects are not equal")
        self.assertTrue(course1.__ne__(course2),
            "The inequality comparison function returns True")
        self.assertTrue(course2.__ne__(course1),
            "The inequality comparison function returns True")

    def test_default_values(self) -> None:
        """Testing the data model with default null values."""
        course = Course()
        self.assertEqual(course.name, '--',
            f"The `name` property has a default value of `{course.name}`")
        self.assertIsNotNone(course.start,
            "The default value of the `start` property is not empty")
        self.assertEqual(course.start.isoformat(), "1970-01-01",
            f"The `start` property has a default value of `{course.start.isoformat()}`")
        self.assertIsNotNone(course.end,
            "The default value of the `end` property is not empty")
        self.assertEqual(course.end.isoformat(), "1970-01-01",
            f"The `end` property has a default value of `{course.end.isoformat()}`")
        self.assertEqual(course.amount, 1,
            f"The `amount` property has a default value of `{course.amount}`")
        self.assertEqual(course.id, -1,
            f"The `id` property has a default value of `{course.id}`")


if __name__ == '__main__':
    unittest.main()
