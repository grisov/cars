import unittest
from sqlite3 import Connection, Cursor
from api.database import Database
from api.models.course import Course
from api.models.search_data import SearchData


class TestDatabase(unittest.TestCase):
    """A set of tests to check the class of interaction with the database."""

    def test_interfaces(self) -> None:
        """Testing the main interfaces for interaction with the database."""
        with Database(":memory:") as db:
            self.assertIsNotNone(db,
                "An instance of a class to interact with the database")
            self.assertIsInstance(db, Database,
                "Check the type of database interaction class")
            self.assertIsNotNone(db._conn,
                "Database connection object")
            self.assertIsInstance(db._conn, Connection,
                "Check the type of the database connection object")
            self.assertIsNotNone(db._cur,
                "The database access cursor object")
            self.assertIsInstance(db._cur, Cursor,
                "Check the type of the database access cursor object")

    def test_get_and_add(self) -> None:
        """Testing the get and add methods."""
        with Database(":memory:") as db:
            self.assertIsNone(db.get(None),  # type: ignore
                "Always return None value if ID is None")
            self.assertIsNone(db.get(0),
                "Always return None value if ID==0")
            self.assertIsNone(db.get(1),
                "The newly created database has no records")

            self.assertIsNone(db.add(None),
                "No action is always taken when trying to add None value")
            course = db.add(
                Course(
                    name="Test",
                    start="2021-02-03",
                    end="2021-12-11",
                    amount=123
                )
            )
            self.assertIsInstance(course, Course,
                "An instance of the Course class is returned after successfull adding")
            id = getattr(course, "id")
            self.assertIsInstance(db.get(id), Course,
                "An entry appeared in the database for the specified ID")
            self.assertEqual(db.get(id), course,
                "The database contains an entry with specified ID that has just been added")
            self.assertIsNone(db.get(id+1),
                "the next entry is missing in the database")
            self.assertIsNone(db.get(id-1),
                "the previous entry is missing in the database")

    def test_delete_method(self) -> None:
        """Testing the method that delete an entry from the database."""
        course = Course(
                name="Test",
                start="2021-02-03",
                end="2021-12-11",
                amount=123
            )
        with Database(":memory:") as db:
            id = getattr(db.add(course), "id")
            db_course = db.get(id)
            self.assertEqual(getattr(db_course, "name"), "Test",
                "The name of the course in the DB coincides with the name of the added course")
            rm_course = db.remove(id)
            self.assertEqual(rm_course, db_course,
                "The deleted entry matches the previously added one")
            self.assertIsNone(db.get(id),
                "The record with ID=={id} is successfully deleted from the database")

    def test_update_method(self) -> None:
        """Testing the method that update an entry in the the database."""
        course1 = Course(
            name="Java for beginners",
            start="2023-02-03",
            end="2023-12-11",
            amount=179
        )
        with Database(":memory:") as db:
            id = getattr(db.add(course1), "id")
            course2 = db.get(id)
            self.assertEqual(course2, course1,
                "The entry in the database is the same as previously added")
            # Changing course data
            setattr(course2, "name", "Python is awesome!")
            setattr(course2, "start", "2021-01-01")
            setattr(course2, "end", "2021-12-31")
            setattr(course2, "amount", 11)
            course = db.update(id, course2)
            self.assertNotEqual(course, course1,
                "The data of the changed course differ from the previous")
            self.assertEqual(course, course2,
                "The data of the changed course is equal to the entered one")

    def test_wrong_id(self) -> None:
        """Attempts to use an incorrect ID or course value."""
        course = Course()
        with Database(":memory:") as db:
            self.assertIsNone(db.update(-1, course),
                "Do nothing for negative ID values")
            self.assertIsNone(db.update(None, course),  # type: ignore
                "Do nothing for ID is None")
            self.assertIsNone(db.update(None, None),  # type: ignore
                "Do nothing if empty ID value and new data")
            self.assertIsNone(db.update(-5, None),
                "Do nothing if the values are negative or empty")

    def test_search_method(self) -> None:
        """Testing the method that searching entries in the database."""
        courses = [
            Course("Python for beginners", "2021-05-01", "2022-07-31", 11),
            Course("Advanced Python", "2023-05-01", "2024-07-31", 22),
            Course("Python forever!", "2025-05-01", "2026-07-31", 33),
            Course("The Python is awesome", "2027-05-01", "2028-07-31", 44),
            Course("Python for enterprise", "2029-05-01", "2030-07-31", 55)
        ]
        with Database(":memory:") as db:
            for course in courses:
                db.add(course)
            self.assertIsInstance(db.search(), list,
                "The search method always returns a list")
            self.assertEqual(len(db.search()), 5,
                "Search without parameters returns all records in the database")
            self.assertEqual(len(db.search(None)), 5,
                "Search with an empty argument returns all records in the database")

            query = SearchData(name = "The Python is awesome")
            self.assertEqual(len(db.search(query)), 1,
                "Search the database by given course name")
            self.assertEqual(db.search(query)[0].amount, 44,
                "The value of the number of lectures in the found course")

            query.name = "Cobol"
            self.assertEqual(len(db.search(query)), 0,
                "Search the database by given course name")

            query.name = "Python"
            self.assertEqual(len(db.search(query)), 5,
                "Search the database by given course name")

            query.start = "2025-01-01"
            self.assertEqual(len(db.search(query)), 3,
                "Search the database by given course name and start date")

            query.end = "2026-07-31"
            self.assertEqual(len(db.search(query)), 1,
                "Search the database by given course name, start and end date")
            self.assertEqual(db.search(query)[0].amount, 33,
                "The value of the number of lectures in the found course")

            query.start = None
            self.assertEqual(len(db.search(query)), 3,
                "Search the database by given course name and end date")


if __name__ == '__main__':
    unittest.main()
