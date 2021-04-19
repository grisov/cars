import unittest
from sqlite3 import Connection, Cursor
from api.database import Database
from api.models.course import Course
from api.models.search_data import SearchData


class TestDatabase(unittest.TestCase):
    """A set of tests to check the class of interaction with the database."""

    def setUp(self):
        """Create an instance of the database interaction class.
        Each time a database will be created in RAM.
        """
        self.db = Database(":memory:")

    def tearDown(self):
        """Closing the connection with the database."""
        self.db.close()

    def test_interfaces(self):
        """Testing the main interfaces for interaction with the database."""
        self.assertIsNotNone(self.db)
        self.assertIsInstance(self.db, Database)
        self.assertIsNotNone(self.db._conn)
        self.assertIsInstance(self.db._conn, Connection)
        self.assertIsNotNone(self.db._cur)
        self.assertIsInstance(self.db._cur, Cursor)

    def test_get_and_add(self):
        """Testing the get and add methods."""
        self.assertIsNone(self.db.get(None))
        self.assertIsNone(self.db.get(0))
        self.assertIsNone(self.db.get(1))

        self.assertIsNone(self.db.add(None))
        course = self.db.add(
            Course(
                name="Test",
                start="2021-02-03",
                end="2021-12-11",
                amount=123
            )
        )
        self.assertIsInstance(course, Course)
        id = course.id
        self.assertIsInstance(self.db.get(id), Course)
        self.assertEqual(self.db.get(id).id, id)
        self.assertEqual(self.db.get(id).name, "Test")
        self.assertEqual(self.db.get(id).start.isoformat(), '2021-02-03')
        self.assertEqual(self.db.get(id).end.isoformat(), '2021-12-11')
        self.assertEqual(self.db.get(id).amount, 123)
        self.assertIsNone(self.db.get(id+1))
        self.assertIsNone(self.db.get(id-1))

    def test_delete_method(self):
        """Testing the method that delete an entry from the database."""
        id = self.db.add(
            Course(
                name="Test",
                start="2021-02-03",
                end="2021-12-11",
                amount=123
            )
        ).id
        course1 = self.db.get(id)
        self.assertEqual(course1.name, "Test")
        course2 = self.db.remove(id)
        self.assertEqual(course1, course2)
        self.assertIsNone(self.db.get(id))

    def test_update_method(self):
        """Testing the method that update an entry in the the database."""
        course1 = Course(
            name="Java for beginners",
            start="2023-02-03",
            end="2023-12-11",
            amount=179
        )
        id = self.db.add(course1).id
        course2 = self.db.get(id)
        self.assertEqual(course2, course1)
        course2.name = "Python is awesome!"
        course2.start = "2021-01-01"
        course2.end = "2021-12-31"
        course2.amount = 11
        course = self.db.update(id, course2)
        self.assertNotEqual(course, course1)
        self.assertEqual(course, course2)

        self.assertIsNone(self.db.update(-1, course))
        self.assertIsNone(self.db.update(None, course))
        self.assertIsNone(self.db.update(None, None))
        self.assertIsNone(self.db.update(-5, None))

    def test_search_method(self):
        """Testing the method that searching entries in the database."""
        self.db.add(Course("Python for beginners", "2021-05-01", "2022-07-31", 11))
        self.db.add(Course("Advanced Python", "2023-05-01", "2024-07-31", 22))
        self.db.add(Course("Python forever!", "2025-05-01", "2026-07-31", 33))
        self.db.add(Course("The Python is awesome", "2027-05-01", "2028-07-31", 44))
        self.db.add(Course("Python for enterprise", "2029-05-01", "2030-07-31", 55))

        self.assertIsInstance(self.db.search(), list)
        self.assertEqual(len(self.db.search()), 5)
        self.assertEqual(len(self.db.search(None)), 5)

        query = SearchData()
        query.name = "The Python is awesome"
        self.assertEqual(len(self.db.search(query)), 1)
        self.assertEqual(self.db.search(query)[0].amount, 44)

        query.name = "COBOL"
        self.assertEqual(len(self.db.search(query)), 0)

        query.name = "Python"
        self.assertEqual(len(self.db.search(query)), 5)

        query.start = "2025-01-01"
        self.assertEqual(len(self.db.search(query)), 3)

        query.end = "2026-07-31"
        self.assertEqual(len(self.db.search(query)), 1)
        self.assertEqual(self.db.search(query)[0].amount, 33)

        query.start = None
        self.assertEqual(len(self.db.search(query)), 3)


if __name__ == '__main__':
    unittest.main()
