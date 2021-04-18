import unittest
from datetime import date
from api.models.base_model import Model
from api.utils import Data


class TestDataValidators(unittest.TestCase):
    """Test case to check data validators."""

    def test_validate_name(self):
        """Testing of the course name validator."""
        self.assertIsInstance(Model.validate_name("ukr"), str)
        self.assertEqual(Model.validate_name("uk"), 'uk')
        self.assertIsNone(Model.validate_name(None))
        with self.assertRaises(ValueError):
            Model.validate_name("")
            Model.validate_name("x")
        with self.assertRaises(TypeError):
            Model.validate_name()
            Model.validate_name(123)
            Model.validate_name(-3.1415)
            Model.validate_name(True)
            Model.validate_name(b'')
            Model.validate_name(bytearray('', encoding='utf-8'))
            Model.validate_name([])
            Model.validate_name({})

    def test_validate_date(self):
        """Testing of the date validator."""
        dt = Data("2021-05-27").deserialize(date)
        self.assertIsInstance(Model.validate_date(dt), date)
        self.assertEqual(Model.validate_date(dt), dt)
        self.assertEqual(Model.validate_date(dt).isoformat(), '2021-05-27')
        self.assertIsInstance(Model.validate_date("2021-04-17"), date)
        self.assertEqual(Model.validate_date("2021-04-17").year, 2021)
        self.assertEqual(Model.validate_date("2021-04-17").month, 4)
        self.assertEqual(Model.validate_date("2021-04-17").day, 17)
        self.assertEqual(Model.validate_date("2021-04-17").isoformat(), '2021-04-17')
        self.assertIsNone(Model.validate_date(None))
        with self.assertRaises(ValueError):
            Model.validate_date("")
            Model.validate_date("2021.04.17")
            Model.validate_date("17-04-2021")
            Model.validate_date("21/04/17")
            Model.validate_date("17 Apr, 2021")
        with self.assertRaises(TypeError):
            Model.validate_date()
            Model.validate_date(-321)
            Model.validate_date(3.1415)
            Model.validate_date(False)
            Model.validate_date(b'')
            Model.validate_date(bytearray('', encoding='utf-8'))
            Model.validate_date([])
            Model.validate_date({})

    def test_validate_amount(self):
        """Testing of the amount validator."""
        self.assertEqual(Model.validate_amount(1), 1)
        self.assertIsInstance(Model.validate_amount(157), int)
        self.assertEqual(Model.validate_amount(255), 255)
        self.assertIsNone(Model.validate_amount(None))
        self.assertEqual(Model.validate_amount("179"), 179)
        self.assertEqual(Model.validate_amount(3.14), 3)
        self.assertEqual(Model.validate_amount(True), 1)

        with self.assertRaises(ValueError):
            Model.validate_amount(0)
            Model.validate_amount(256)
            Model.validate_amount(-137)
            Model.validate_amount("-3.14")
            Model.validate_amount(False)
        with self.assertRaises(TypeError):
            Model.validate_amount()
            Model.validate_amount('')
            Model.validate_amount("Test")
            Model.validate_amount(b'')
            Model.validate_amount(bytearray('', encoding='utf-8'))
            Model.validate_amount([])
            Model.validate_amount({})


if __name__ == '__main__':
    unittest.main()
