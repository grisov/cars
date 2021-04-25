import unittest
from typing import Collection, Dict, List, Union
from datetime import date, datetime
from api.utils import GenericType, Data


class TestDataClass(unittest.TestCase):
    """A test case for the api.utils.Data class."""

    def test_getter(self) -> None:
        """Testing the getter."""
        data = Data(123)
        self.assertIsNotNone(data.value,
            "Getter returns a non-empty value")
        self.assertEqual(data.value, 123,
            "The returned value corresponds to the original")
        with self.assertRaises(AttributeError):
            data.value = 'hello'  # type: ignore

    def test_primitive_types(self) -> None:
        data = Data(0)
        for primitive_type in (int, float, str, bool, bytearray):
            self.assertIn(primitive_type, data._primitive_types,
                "Each of these types is primitive")
        for value in (792, 145.97, 'awesome', False, bytearray(b'love')):
            self.assertIn(type(value), data._primitive_types,
                "Each of these values has a primitive type")
        for any_type in (object, List, Dict, Union, GenericType):
            self.assertNotIn(any_type, data._primitive_types,
                "All these types are not primitive")

    def test_deserialize_primitive_float(self) -> None:
        """Deserialization of the float primitive type."""
        data = Data(1.0)
        self.assertEqual(data.deserialize_primitive(int), 1,
            "Convert to an integer")
        self.assertEqual(data.deserialize_primitive(float), 1.0,
            "Convert to a float")
        self.assertEqual(data.deserialize_primitive(str), '1.0',
            "Convert to a string")
        self.assertEqual(data.deserialize_primitive(bool), True,
            "Convert to a boolean")
        self.assertEqual(data.deserialize_primitive(bytearray), 1.0,
            "Convert to a bytearray")

    def test_deserialize_primitive_str(self) -> None:
        """Deserialization of the string primitive type."""
        data = Data("783.15")
        self.assertEqual(data.deserialize_primitive(int), "783.15",
            "Can't convert to an integer")
        self.assertEqual(data.deserialize_primitive(float), 783.15,
            "Convert to a float")
        self.assertEqual(data.deserialize_primitive(str), "783.15",
            "Convert to a string")
        self.assertEqual(data.deserialize_primitive(bool), True,
            "Convert to a boolean")
        self.assertEqual(data.deserialize_primitive(bytearray), "783.15",
            "Can't convert to a bytearray type")

    def test_deserialize_date_iso(self) -> None:
        """Deserialization of the ISO formated date type."""
        dt = Data("2037-07-01").deserialize_date()
        self.assertIsNotNone(dt,
            "Date object is not empty")
        self.assertIsInstance(dt, date,
            "Check of the object type")
        self.assertEqual(getattr(dt, "year"), 2037,
            "The value of the year from the date object")
        self.assertEqual(getattr(dt, "month"), 7,
            "The value of the month from the date object")
        self.assertEqual(getattr(dt, "day"), 1,
            "The value of the day from the date object")
        self.assertEqual(getattr(dt, "isoformat")(), "2037-07-01",
            "Show the date in ISO format")

    def test_deserialize_date_noniso(self) -> None:
        """Deserialization of the non-ISO formated date type."""
        dt = Data("17.03.2019").deserialize_date()
        self.assertIsNotNone(dt,
            "Date object is not empty")
        self.assertIsInstance(dt, str,
            "Check of the object type")
        self.assertEqual(dt, "17.03.2019",
            "The value could not be deserialized")

    def test_deserialize_datetime_iso(self) -> None:
        """Deserialization of the ISO formated datetime type."""
        dt = Data("2021-11-23T17:25:47").deserialize_datetime()
        self.assertIsNotNone(dt,
            "Datetime object is not empty")
        self.assertIsInstance(dt, datetime,
            "Check of the object type")
        self.assertEqual(getattr(dt, "year"), 2021,
            "The value of the year from the datetime object")
        self.assertEqual(getattr(dt, "month"), 11,
            "The value of the month from the datetime object")
        self.assertEqual(getattr(dt, "day"), 23,
            "The value of the day from the datetime object")
        self.assertEqual(getattr(dt, "hour"), 17,
            "The value of the hour from the datetime object")
        self.assertEqual(getattr(dt, "minute"), 25,
            "The value of the minute from the datetime object")
        self.assertEqual(getattr(dt, "second"), 47,
            "The value of the second from the datetime object")

    def test_deserialize_datetime_noniso(self) -> None:
        """Deserialization of the non-ISO formated datetime type."""
        dt = Data("15.09.2021 11:47:15").deserialize_datetime()
        self.assertIsNotNone(dt,
            "Datetime object is not empty")
        self.assertIsInstance(dt, str,
            "Check of the object type")
        self.assertEqual(dt, "15.09.2021 11:47:15",
            "The value could not be deserialized")

    def test_deserialize(self) -> None:
        """General method of data deserialization."""
        self.assertIsNone(Data(None).deserialize(bytearray),
            "Converting None to any type also returns None")
        self.assertEqual(Data("Hello!").deserialize(str), "Hello!",
            "Convert string to string")
        self.assertEqual(Data("51735").deserialize(int), 51735,
            "Convert integer to integer")
        self.assertEqual(Data("2021-04-17").deserialize(date).day, 17,
            "Convert an ISO date string to type date")
        self.assertEqual(Data("2021-05-17T12:21:57").deserialize(datetime).second, 57,
            "Convert an ISO datetime string to type datetime")


class TestGenericType(unittest.TestCase):
    """A test case for the api.utils.GenericType class."""

    def test_getter(self) -> None:
        """Testing the getter method."""
        gt = GenericType(bool)
        self.assertIsNotNone(gt.value,
            "The `value` attribute is not empty")
        self.assertEqual(gt.value, bool,
            "The value of the `value` attribute")
        with self.assertRaises(AttributeError):
            gt.value = int  # type: ignore

    def test_is_generic(self) -> None:
        """Testing the correctness of the definition of generic types."""
        self.assertTrue(GenericType(List).is_generic(),
            "The type `List` is generic")
        self.assertTrue(GenericType(Collection).is_generic(),
            "The type `Collection` is generic")
        self.assertFalse(GenericType(bytes).is_generic(),
            "The type `bytes` is not generic")
        self.assertFalse(GenericType(str).is_generic(),
            "The type `str` is not generic")
        self.assertFalse(GenericType(object).is_generic(),
            "The type `object` is not generic")

    def test_is_dict(self) -> None:
        """Checking the correctness of the definition of the generic dict type."""
        self.assertTrue(GenericType(Dict).is_dict(),
            "The type `Dict` is a generic dict")
        self.assertFalse(GenericType(List).is_dict(),
            "The type `List` is not a generic dict")
        self.assertFalse(GenericType(dict).is_dict(),
            "The type `dict` is not a generic dict")
        self.assertFalse(GenericType(float).is_dict(),
            "The type `float` is not a generic dict")

    def test_is_list(self) -> None:
        """Checking the correctness of the definition of the generic list type."""
        self.assertTrue(GenericType(List).is_list(),
            "The type `List` is a generic list")
        self.assertFalse(GenericType(Dict).is_list(),
            "The type `Dict` is not a generic list")
        self.assertFalse(GenericType(list).is_list(),
            "The type `list` is not a generic list")
        self.assertFalse(GenericType(bool).is_list(),
            "The type `bool` is not a generic list")


if __name__ == '__main__':
    unittest.main()
