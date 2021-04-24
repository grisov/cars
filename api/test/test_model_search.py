import unittest
from datetime import date
from api.models.search_data import SearchData
from api.utils import Data


class TestSearchDataModel(unittest.TestCase):
    """Test case for testing the SearchData model."""

    def test_attributes(self) -> None:
        """Testing the attributes of the data model."""
        sd = SearchData(
            name="Technology",
            start="2021-04-28",
            end="2021-05-15"
        )
        self.assertIsInstance(sd.name, str,
            "Check the data type of the model property")
        self.assertEqual(sd.name, "Technology",
            f"The name to search is `{sd.name}`")

        self.assertIsInstance(sd.start, date,
            "Check the data type of the model property")
        self.assertEqual(sd.start.isoformat(), "2021-04-28",
            f"The start date for search is {sd.start.isoformat()}")
        sd.start = Data("2021-04-28").deserialize(date)
        self.assertIsInstance(sd.start, date,
            "Check the data type of the model property")
        self.assertEqual(sd.start.year, 2021,
            f"The start year is {sd.start.year}")
        self.assertEqual(sd.start.month, 4,
            f"The start month is {sd.start.month}")
        self.assertEqual(sd.start.day, 28,
            f"The start day is {sd.start.day}")

        self.assertIsInstance(sd.end, date,
            "Check the data type of the model property")
        self.assertEqual(sd.end.isoformat(), "2021-05-15",
            f"The end date for search is {sd.start.isoformat()}")
        sd.end = Data("2021-07-17").deserialize(date)
        self.assertIsInstance(sd.end, date,
            "Check the data type of the model property")
        self.assertEqual(sd.end.year, 2021,
            f"The end year to search is {sd.end.year}")
        self.assertEqual(sd.end.month, 7,
            f"The end month to search is {sd.end.month}")
        self.assertEqual(sd.end.day, 17,
            f"The end day to search is {sd.end.day}")

    def test_valid_name_values(self) -> None:
        """Testing the valid values of the name attribute."""
        sd = SearchData()
        sd.name="Yalantis"
        self.assertEqual(sd.name, 'Yalantis',
            f"The current name to search is `{sd.name}`")
        sd.name=None
        self.assertIsNone(sd.name,
            "The name to search is empty")
        sd.name="asd"
        self.assertEqual(sd.name, 'asd',
            f"The current name to search is `{sd.name}`")
        with self.assertRaises(ValueError):
            sd.name='x'  # len < 2 characters
            sd.name=''  # len < 2 characters
        self.assertIsNotNone(sd.name,
            "Name for search is not empty")
        self.assertIsInstance(sd.name, (str),
            "Check the data type of the model property")

    def test_comparison_start_end(self) -> None:
        """Testing the comparison of start and end dates."""
        sd = SearchData()
        sd.end = "2021-05-05"
        sd.start = "2021-05-05"  # start == end
        sd.end = "2021-05-06"  # end > start
        with self.assertRaises(ValueError):
            sd.end = "2021-05-04"  # day 4 < 5
            sd.end = "2021-04-05"  # month 4 < 5
            sd.end = "2020-05-05"  # year 2020 < 2021
            SearchData(start="2021-07-07", end="2021-07-06")  # end < start

        sd = SearchData()
        sd.end = Data("2021-05-05").deserialize(date)
        sd.start = Data("2021-05-05").deserialize(date)  # start == end
        sd.end = Data("2021-05-06").deserialize(date)  # end > start
        with self.assertRaises(ValueError):
            sd.end = Data("2021-05-04").deserialize(date)  # day 4 < 5
            sd.end = Data("2021-04-05").deserialize(date)  # month 4 < 5
            sd.end = Data("2020-05-05").deserialize(date)  # year 2020 < 2021
            SearchData(
                start=Data("2021-07-07").deserialize(date),
                end=Data("2021-07-06").deserialize(date)
            )  # end < start

    def test_openapi_types(self) -> None:
        """Testing declared attribute types."""
        sd = SearchData(
            name="Yalantis",
            start=Data("2021-05-07").deserialize(date),
            end=Data("2021-11-29").deserialize(date)
        )
        self.assertTrue(hasattr(sd, "openapi_types"),
            "The model contains the `openapi_types` attribute")
        self.assertIsInstance(sd.openapi_types, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(sd.openapi_types), 3,
            f"The length of the openapi_types dict is {len(sd.openapi_types)}")
        self.assertIn("name", sd.openapi_types,
            "The `name` key is present in the openapi_types dict")
        self.assertIn("start", sd.openapi_types,
            "The `start` key is present in the openapi_types dict")
        self.assertIn("end", sd.openapi_types,
            "The `end` key is present in the openapi_types dict")
        self.assertEqual(sd.openapi_types["name"], str,
            "Check the value in the openapi_types dict")
        self.assertEqual(sd.openapi_types["start"], date,
            "Check the value in the openapi_types dict")
        self.assertEqual(sd.openapi_types["end"], date,
            "Check the value in the openapi_types dict")

    def test_attribute_map(self) -> None:
        """Testing declared attribute names."""
        sd = SearchData(
            name="Yalantis",
            start=Data("2021-05-07").deserialize(date),
            end=Data("2021-11-29").deserialize(date)
        )
        self.assertTrue(hasattr(sd, "attribute_map"),
            "The model contains the `attribute_map` attribute")
        self.assertIsInstance(sd.attribute_map, dict,
            "Check the data type of the model attribute")
        self.assertEqual(len(sd.attribute_map), 3,
            f"The length of the attribute_map dict is {len(sd.attribute_map)}")
        self.assertIn("name", sd.attribute_map,
            "The `name` key is present in the attribute_map dict")
        self.assertIn("start", sd.attribute_map,
            "The `start` key is present in the attribute_map dict")
        self.assertIn("end", sd.attribute_map,
            "The `end` key is present in the attribute_map dict")
        self.assertEqual(sd.attribute_map["name"], 'name',
            f"Under the `name` key there is a value of `{sd.attribute_map['name']}`")
        self.assertEqual(sd.attribute_map["start"], 'start',
            f"Under the `start` key there is a value of `{sd.attribute_map['start']}`")
        self.assertEqual(sd.attribute_map["end"], 'end',
            f"Under the `end` key there is a value of `{sd.attribute_map['end']}`")

    def test_from_to_dict(self) -> None:
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "name": "Quality Assurance",
            "start": Data("2021-05-07").deserialize(date),
            "end": Data("2021-11-29").deserialize(date)
        }
        sd = SearchData.from_dict(data)
        self.assertIsInstance(sd, SearchData,
            "Check the type of the variable")
        self.assertEqual(sd.name, 'Quality Assurance',
            f"The name to search is `{sd.name}`")
        self.assertEqual(sd.start, data['start'],
            f"The start date to search is `{sd.start.isoformat()}`")
        self.assertEqual(sd.end, data['end'],
            f"The end date to search is `{sd.end.isoformat()}`")
        info = sd.to_dict()
        self.assertIsInstance(info, dict,
            "Check the type of the variable")
        self.assertEqual(info['name'], 'Quality Assurance',
            f"The `name` key contains a value of `{info['name']}`")
        self.assertEqual(info['start'], data['start'],
            f"The `start` key contains a value of `{info['start'].isoformat()}`")
        self.assertEqual(info['end'], data['end'],
            f"The `end` key contains a value of `{info['end'].isoformat()}`")

    def test_to_str(self) -> None:
        """Testing the method of converting the model to a string."""
        sd = SearchData(
            name="Quality Assurance",
            start="2021-05-07",
            end="2021-11-29"
        )
        line = "{'name': 'Quality Assurance', 'start': '2021-05-07', 'end': '2021-11-29'}"
        self.assertIsInstance(sd, SearchData,
            "Check the data type of the variable")
        self.assertIsInstance(line, str,
            "Check the data type of the variable")
        self.assertEqual(sd.to_str(), line,
            f"The to_str() method returns the following value: `{sd.to_str()}`")
        self.assertEqual(sd.__repr__(), line,
            f"The __repr__() method returns the following value: `{sd.__repr__()}`")
        self.assertEqual(str(sd), line,
            f"Convert to a string returns the following value: `{str(sd)}`")

    def test_eq_models(self) -> None:
        """Testing to check models for equality."""
        sd1 = SearchData(
            name="Python is awesome!",
            start=Data("2021-09-03").deserialize(date),
            end=Data("2021-12-23").deserialize(date)
        )
        sd2 = SearchData(
            name="Python is awesome!",
            start=Data("2021-09-03").deserialize(date),
            end=Data("2021-12-23").deserialize(date)
        )
        self.assertEqual(sd1.name, sd2.name,
            f"The `name` property has a value of `{sd1.name}`")
        self.assertEqual(sd1.start, sd2.start,
            f"The `start` property has a value of `{sd1.start.isoformat()}`")
        self.assertEqual(sd1.end, sd2.end,
            f"The `end` property has a value of `{sd1.end.isoformat()}`")
        self.assertTrue(sd1 == sd2,
            "Both objects are the same")
        self.assertTrue(sd1.__eq__(sd2),
            f"The equality comparison function returns {str(sd1.__eq__(sd2))}")

    def test_ne_models(self) -> None:
        """Testing to check models for inequality."""
        sd1 = SearchData(
            name="Python is awesome!",
            start=Data("2021-09-03").deserialize(date),
            end=Data("2021-12-23").deserialize(date)
        )
        sd2 = SearchData(
            name="OpenAPI/Swagger",
            start=Data("2021-07-11").deserialize(date),
            end=Data("2021-12-23").deserialize(date)
        )
        self.assertNotEqual(sd1.name, sd2.name,
            "The `name` properties have the differ values")
        self.assertNotEqual(sd1.start, sd2.start,
            "The `start` properties have the differ values")
        self.assertEqual(sd1.end, sd2.end,
            "The `end` properties have the same values")
        self.assertFalse(sd1 == sd2,
            "Objects are different")
        self.assertTrue(sd1 != sd2,
            "Objects are not equal")
        self.assertTrue(sd1.__ne__(sd2),
            f"The inequality comparison function returns {str(sd1.__ne__(sd2))}")
        self.assertTrue(sd2.__ne__(sd1),
            f"The inequality comparison function returns {str(sd2.__ne__(sd1))}")

    def test_none_values(self) -> None:
        """Testing the data model with None values."""
        sd = SearchData()
        self.assertIsNone(sd.name,
            "The `name` property has empty value")
        self.assertIsNone(sd.start,
            "The `start` property has empty value")
        self.assertIsNone(sd.end,
            "The `end` property has empty value")


if __name__ == '__main__':
    unittest.main()
