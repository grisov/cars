import unittest
from datetime import date
from api.models.search_data import SearchData
from api.utils import Data


class TestSearchDataModel(unittest.TestCase):
    """Test case for testing the SearchData model."""

    def test_attributes(self):
        """Testing the attributes of the data model."""
        sd = SearchData(
            name="Technology",
            start="2021-04-28",
            end="2021-05-15"
        )
        self.assertIsInstance(sd.name, str)
        self.assertEqual(sd.name, "Technology")

        self.assertIsInstance(sd.start, date)
        self.assertEqual(sd.start.isoformat(), "2021-04-28")
        sd.start = Data("2021-04-28").deserialize(date)
        self.assertIsInstance(sd.start, date)
        self.assertEqual(sd.start.year, 2021)
        self.assertEqual(sd.start.month, 4)
        self.assertEqual(sd.start.day, 28)

        self.assertIsInstance(sd.end, date)
        self.assertEqual(sd.end.isoformat(), "2021-05-15")
        sd.end = Data("2021-07-17").deserialize(date)
        self.assertIsInstance(sd.end, date)
        self.assertEqual(sd.end.year, 2021)
        self.assertEqual(sd.end.month, 7)
        self.assertEqual(sd.end.day, 17)

    def test_valid_name_values(self):
        """Testing the valid values of the name attribute."""
        sd = SearchData()
        sd.name="Yalantis"
        self.assertEqual(sd.name, 'Yalantis')
        sd.name=None
        self.assertIsNone(sd.name)
        sd.name="asd"
        self.assertEqual(sd.name, 'asd')
        with self.assertRaises(ValueError):
            sd.name='x'
            sd.name=''
        self.assertIsNotNone(sd.name)
        self.assertIsInstance(sd.name, (str))

    def test_comparison_start_end(self):
        """Testing the comparison of start and end dates."""
        sd = SearchData()
        sd.end = "2021-05-05"
        sd.start = "2021-05-05"
        sd.end = "2021-05-06"
        with self.assertRaises(ValueError):
            sd.end = "2021-05-04"
            sd.end = "2021-04-05"
            sd.end = "2020-05-05"
            SearchData(start="2021-07-07", end="2021-07-06")

        sd = SearchData()
        sd.end = Data("2021-05-05").deserialize(date)
        sd.start = Data("2021-05-05").deserialize(date)
        sd.end = Data("2021-05-06").deserialize(date)
        with self.assertRaises(ValueError):
            sd.end = Data("2021-05-04").deserialize(date)
            sd.end = Data("2021-04-05").deserialize(date)
            sd.end = Data("2020-05-05").deserialize(date)
            SearchData(
                start=Data("2021-07-07").deserialize(date),
                end=Data("2021-07-06").deserialize(date)
            )

    def test_openapi_types(self):
        """Testing declared attribute types."""
        sd = SearchData(
            name="Yalantis",
            start=Data("2021-05-07").deserialize(date),
            end=Data("2021-11-29").deserialize(date)
        )
        self.assertTrue(hasattr(sd, "openapi_types"))
        self.assertIsInstance(sd.openapi_types, dict)
        self.assertEqual(len(sd.openapi_types), 3)
        self.assertIn("name", sd.openapi_types)
        self.assertIn("start", sd.openapi_types)
        self.assertIn("end", sd.openapi_types)
        self.assertEqual(sd.openapi_types["name"], str)
        self.assertEqual(sd.openapi_types["start"], date)
        self.assertEqual(sd.openapi_types["end"], date)

    def test_attribute_map(self):
        """Testing declared attribute names."""
        sd = SearchData(
            name="Yalantis",
            start=Data("2021-05-07").deserialize(date),
            end=Data("2021-11-29").deserialize(date)
        )
        self.assertTrue(hasattr(sd, "attribute_map"))
        self.assertIsInstance(sd.attribute_map, dict)
        self.assertEqual(len(sd.attribute_map), 3)
        self.assertIn("name", sd.attribute_map)
        self.assertIn("start", sd.attribute_map)
        self.assertIn("end", sd.attribute_map)
        self.assertEqual(sd.attribute_map["name"], 'name')
        self.assertEqual(sd.attribute_map["start"], 'start')
        self.assertEqual(sd.attribute_map["end"], 'end')

    def test_from_to_dict(self):
        """Testing methods of model conversion into a dict and vice versa."""
        data = {
            "name": "Quality Assurance",
            "start": Data("2021-05-07").deserialize(date),
            "end": Data("2021-11-29").deserialize(date)
        }
        sd = SearchData.from_dict(data)
        self.assertIsInstance(sd, SearchData)
        self.assertEqual(sd.name, 'Quality Assurance')
        self.assertEqual(sd.start, data['start'])
        self.assertEqual(sd.end, data['end'])
        info = sd.to_dict()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['name'], 'Quality Assurance')
        self.assertEqual(info['start'], data['start'])
        self.assertEqual(info['end'], data['end'])

    def test_to_str(self):
        """Testing the method of converting the model to a string."""
        sd = SearchData(
            name="Quality Assurance",
            start="2021-05-07",
            end="2021-11-29"
        )
        line = "{'name': 'Quality Assurance', 'start': '2021-05-07', 'end': '2021-11-29'}"
        self.assertIsInstance(sd, SearchData)
        self.assertIsInstance(line, str)
        self.assertEqual(sd.to_str(), line)
        self.assertEqual(sd.__repr__(), line)
        self.assertEqual(str(sd), line)

    def test_eq_models(self):
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
        self.assertEqual(sd1.name, sd2.name)
        self.assertEqual(sd1.start, sd2.start)
        self.assertEqual(sd1.end, sd2.end)
        self.assertTrue(sd1 == sd2)
        self.assertTrue(sd1.__eq__(sd2))

    def test_ne_models(self):
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
        self.assertNotEqual(sd1.name, sd2.name)
        self.assertNotEqual(sd1.start, sd2.start)
        self.assertEqual(sd1.end, sd2.end)
        self.assertFalse(sd1 == sd2)
        self.assertTrue(sd1 != sd2)
        self.assertTrue(sd1.__ne__(sd2))
        self.assertTrue(sd2.__ne__(sd1))

    def test_none_values(self):
        """Testing the data model with None values."""
        sd = SearchData()
        self.assertIsNone(sd.name)
        self.assertIsNone(sd.start)
        self.assertIsNone(sd.end)


if __name__ == '__main__':
    unittest.main()
