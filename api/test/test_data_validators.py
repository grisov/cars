import unittest
from datetime import date
from api.models.base_model import Model
from api.utils import Data


class TestDataValidators(unittest.TestCase):
    """Test case to check data validators."""

    def test_validate_name(self) -> None:
        """Testing of the course name validator."""
        self.assertIsInstance(Model.validate_name("ukr"), str,
            "Check the type of the name field")
        self.assertEqual(Model.validate_name("uk"), 'uk',
            "Validation of a string that contains only two characters")
        self.assertIsNone(Model.validate_name(None),
            "Validation of the None value")
        with self.assertRaises(ValueError):
            Model.validate_name("")  # empty string
            Model.validate_name("x")  # one character
        with self.assertRaises(TypeError):
            Model.validate_name()  # type: ignore
            Model.validate_name(123)  # type: ignore
            Model.validate_name(-3.1415)  # type: ignore
            Model.validate_name(True)  # type: ignore
            Model.validate_name(b'')  # type: ignore
            Model.validate_name(bytearray('', encoding='utf-8'))  # type: ignore
            Model.validate_name([])  # type: ignore
            Model.validate_name({})  # type: ignore

    def test_validate_date(self) -> None:
        """Testing of the date validator."""
        dt = Data("2021-05-27").deserialize(date)
        self.assertIsInstance(Model.validate_date(dt), date,
            "Check the date value type")
        self.assertEqual(Model.validate_date(dt), dt,
            "Check a value that has a date type")
        self.assertEqual(getattr(Model.validate_date(dt), "isoformat")(), '2021-05-27',
            "Checking the correctness of the value in the ISO format")
        self.assertIsInstance(Model.validate_date("2021-04-17"), date,
            "Check the conversion of the ISO formated string to date type")
        self.assertEqual(getattr(Model.validate_date("2021-04-17"), "year"), 2021,
            "Check the converted value of the year field")
        self.assertEqual(getattr(Model.validate_date("2021-04-17"), "month"), 4,
            "Check the converted value of the month field")
        self.assertEqual(getattr(Model.validate_date("2021-04-17"), "day"), 17,
            "Check the converted value of the day field")
        self.assertEqual(getattr(Model.validate_date("2021-04-17"), "isoformat")(), '2021-04-17',
            "Checking the output of the isoformat() method")
        self.assertIsNone(Model.validate_date(None),
            "Check for deserialization of the None value")
        with self.assertRaises(ValueError):
            Model.validate_date("")  # empty string
            Model.validate_date("2021.04.17")  # non-ISO format
            Model.validate_date("17-04-2021")  # non-ISO format
            Model.validate_date("21/04/17")  # non-ISO format
            Model.validate_date("17 Apr, 2021")  # non-ISO format
        with self.assertRaises(TypeError):
            Model.validate_date()  # type: ignore
            Model.validate_date(-321)  # type: ignore
            Model.validate_date(3.1415)  # type: ignore
            Model.validate_date(False)  # type: ignore
            Model.validate_date(b'')  # type: ignore
            Model.validate_date(bytearray('', encoding='utf-8'))  # type: ignore
            Model.validate_date([])  # type: ignore
            Model.validate_date({})  # type: ignore

    def test_validate_amount(self) -> None:
        """Testing of the amount validator."""
        self.assertEqual(Model.validate_amount(1), 1,
            "The minimum allowable value of the amount field")
        self.assertIsInstance(Model.validate_amount(157), int,
            "Check the type of the allowable value of the amount field")
        self.assertEqual(Model.validate_amount(255), 255,
            "The maximum allowable value of the amount field")
        self.assertIsNone(Model.validate_amount(None),
            "None value is allowed")
        self.assertEqual(Model.validate_amount("179"), 179,  # type: ignore
            "Check the deserialization of an integer value")
        self.assertEqual(Model.validate_amount(3.14), 3,  # type: ignore
            "Check the deserialization of a float value")
        self.assertEqual(Model.validate_amount(True), 1,
            "Check the deserialization of a boolean value")

        with self.assertRaises(ValueError):
            Model.validate_amount(0)  # less 1 is not allowed
            Model.validate_amount(256)  # greater 255 is not allowed
            Model.validate_amount(-137)  # less 1 is not allowed
            Model.validate_amount("-3.14")  # type: ignore
            Model.validate_amount(False)  # int(False)==0
        with self.assertRaises(TypeError):
            Model.validate_amount()  # type: ignore
            Model.validate_amount('')  # type: ignore
            Model.validate_amount("Test")  # type: ignore
            Model.validate_amount(b'')  # type: ignore
            Model.validate_amount(bytearray('', encoding='utf-8'))  # type: ignore
            Model.validate_amount([])  # type: ignore
            Model.validate_amount({})  # type: ignore


if __name__ == '__main__':
    unittest.main()
