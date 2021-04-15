import unittest
from typing import Dict, List, Union
from datetime import date, datetime
from api.utils import GenericType, Data


class TestGenericType(unittest.TestCase):
    """A test case for the api.utils.GenericType class."""

    def test_getter(self):
        gt = GenericType(Union)
        self.assertIsNotNone(gt.value)
        self.assertEqual(gt.value, Union)
        with self.assertRaises(AttributeError):
            gt.value=int

    def test_is_generic(self):
        self.assertTrue(GenericType(List).is_generic())
        self.assertFalse(GenericType(Union).is_generic())
        self.assertFalse(GenericType(str).is_generic())
        self.assertFalse(GenericType(object).is_generic())

    def test_is_dict(self):
        self.assertTrue(GenericType(Dict).is_dict())
        self.assertFalse(GenericType(List).is_dict())
        self.assertFalse(GenericType(dict).is_dict())
        self.assertFalse(GenericType(float).is_dict())

    def test_is_list(self):
        self.assertTrue(GenericType(List).is_list())
        self.assertFalse(GenericType(Dict).is_list())
        self.assertFalse(GenericType(list).is_list())
        self.assertFalse(GenericType(bool).is_list())


class TestDataClass(unittest.TestCase):
    """A test case for the api.utils.Data class."""

    def test_getter(self):
        data = Data(123)
        self.assertIsNotNone(data.value)
        self.assertEqual(data.value, 123)
        with self.assertRaises(AttributeError):
            data.value='hello'

    def test_primitive_types(self):
        data = Data(0)
        for primitive_type in (int, float, str, bool, bytearray):
            self.assertIn(primitive_type, data._primitive_types)
        for value in (792, 145.97, 'awesome', False, bytearray(b'love')):
            self.assertIn(type(value), data._primitive_types)
        for any_type in (object, List, Dict, Union, GenericType):
            self.assertNotIn(any_type, data._primitive_types)

    def test_deserialize_primitive_float(self):
        data = Data(1.0)
        self.assertEqual(data.deserialize_primitive(int), 1)
        self.assertEqual(data.deserialize_primitive(float), 1.0)
        self.assertEqual(data.deserialize_primitive(str), '1.0')
        self.assertEqual(data.deserialize_primitive(bool), True)
        self.assertEqual(data.deserialize_primitive(bytearray), 1.0)

    def test_deserialize_primitive_str(self):
        data = Data("783.15")
        self.assertEqual(data.deserialize_primitive(int), "783.15")
        self.assertEqual(data.deserialize_primitive(float), 783.15)
        self.assertEqual(data.deserialize_primitive(str), "783.15")
        self.assertEqual(data.deserialize_primitive(bool), True)
        self.assertEqual(data.deserialize_primitive(bytearray), "783.15")

    def test_deserialize_date_iso(self):
        dt = Data("2037-07-01").deserialize_date()
        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, date)
        self.assertEqual(dt.year, 2037)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 1)

    def test_deserialize_date_noniso(self):
        dt = Data("17.03.2019").deserialize_date()
        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, str)
        self.assertEqual(dt, "17.03.2019")

    def test_deserialize_datetime_iso(self):
        dt = Data("2021-11-23T17:25:47").deserialize_datetime()
        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 11)
        self.assertEqual(dt.day, 23)
        self.assertEqual(dt.hour, 17)
        self.assertEqual(dt.minute, 25)
        self.assertEqual(dt.second, 47)

    def test_deserialize_datetime_noniso(self):
        dt = Data("15.09.2021 11:47:15").deserialize_date()
        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, str)
        self.assertEqual(dt, "15.09.2021 11:47:15")

    def test_deserialize(self):
        self.assertIsNone(Data(None).deserialize(bytearray))
        self.assertEqual(Data("Hello!").deserialize(str), "Hello!")
        self.assertEqual(Data("51735").deserialize(int), 51735)
        self.assertEqual(Data("2021-04-17").deserialize(date).day, 17)
        self.assertEqual(Data("2021-05-17T12:21:57").deserialize(datetime).second, 57)


if __name__ == '__main__':
    unittest.main()
