from flask import json
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.database import Database


class TestUpdateController(BaseTestCase):
    """Set of tests to check the 'update' controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        super(TestUpdateController, self).setUp()
        self.headers["Content-Type"] = "application/json"
        # Filling the database
        courses = [
            Course("Python forever!", "2021-06-07", "2023-09-27", 44),
            Course("Framework Django", "2022-05-05", "2024-11-19", 25),
            Course("Machine Learning", "2023-06-07", "2025-10-17", 19)
        ]
        with Database() as db:
            for course in courses:
                db.add(course)

    def test_without_parameters(self) -> None:
        """Try to make update request without parameters."""
        response = self.client.put(
            "/api/v1/course",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert404(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/problem+json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/problem+json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(error.status, 404,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Not Found",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

    def test_exist_course_to_none(self) -> None:
        """Try updating an existing entry to empty."""
        id = 2
        response = self.client.put(
            "/api/v1/course/%d" % id,
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/problem+json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/problem+json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(error.status, 400,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Bad Request",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

        with Database() as db:
            course = db.get(id)
        self.assertIsNotNone(course,
            "An entry with the specified ID is still exist in the DB")
        self.assertEqual(course.name, "Framework Django",
            "The name of the course in the DB is not changed")

    def test_non_exist_course_to_none(self) -> None:
        """Try updating a non-existing entry to empty."""
        response = self.client.put(
            "/api/v1/course/456",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/problem+json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/problem+json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(error.status, 400,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Bad Request",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

    def test_exist_course_to_valid(self) -> None:
        """Update an existing course to a new valid one."""
        id = 3
        with Database() as db:
            old_course = db.get(id)
        self.assertIsNotNone(old_course,
            f"The record with ID={id} is exists in the DB")
        new_course = Course(
            name="Features of Python 3.10",
            start="2022-02-03",
            end="2022-04-05",
            amount=7
        )
        response = self.client.put(
            "/api/v1/course/%d" % id,
            headers=self.headers,
            data=json.dumps(new_course.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        course = Course(**response.json)
        with Database() as db:
            db_course = db.get(id)
        self.assertEqual(course.id, db_course.id,
            f"The ID of the updated course is `{course.id}`")
        self.assertNotEqual(course.name, old_course.name,
            "The current course name does not match the previous data")
        self.assertEqual(course.name, db_course.name,
            f"The name of the updated course is `{course.name}`")
        self.assertNotEqual(course.start, old_course.start,
            "The current course start date does not match the previous data")
        self.assertEqual(course.start, db_course.start,
            f"The start date of the updated course is `{course.start}`")
        self.assertNotEqual(course.end, old_course.end,
            "The current course gratuation date does not match the previous data")
        self.assertEqual(course.end, db_course.end,
            f"The gratuation date of the updated course is `{course.end}`")
        self.assertNotEqual(course.amount, old_course.amount,
            "The current number of lectures does not match the previous data")
        self.assertEqual(course.amount, db_course.amount,
            f"Number of lectures in the updated course are `{course.amount}`")

    def test_non_exist_course_to_valid(self) -> None:
        """Try to update a non-existing course to a new valid one.
        The course will be added to the database and automatically assigned new ID.
        """
        id = 795
        with Database() as db:
            old_course = db.get(id)
        self.assertIsNone(old_course,
            "There is no record in the database with the specified ID")
        new_course = Course(
            name="Features of Python 3.10",
            start="2022-02-03",
            end="2022-04-05",
            amount=7
        )
        response = self.client.put(
            "/api/v1/course/%d" % id,
            headers=self.headers,
            data=json.dumps(new_course.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        course = Course(**response.json)
        with Database() as db:
            db_course = db.get(course.id)
        self.assertNotEqual(course.id, id,
            f"The record was assigned to ID={course.id}, which is different from the original {id}")
        self.assertEqual(course, db_course,
            "The data in the response is identical to the record in the database")

    def test_exist_course_to_incomplete(self) -> None:
        """Submit incomplete data to update an existing record."""
        id = 3
        with Database() as db:
            old_course = db.get(id)
        self.assertIsNotNone(old_course,
            f"There is an entry with an ID={id} in the database")
        incomplete_data = {
            "name": "Features of Python 3.10",
            "end": "2022-04-05"
        }
        response = self.client.put(
            "/api/v1/course/%d" % id,
            headers=self.headers,
            data=json.dumps(incomplete_data),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/problem+json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/problem+json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(error.status, 400,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Bad Request",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

        with Database() as db:
            course = db.get(id)
        self.assertIsNotNone(course,
            "An entry with the specified ID is still exist in the DB")
        self.assertEqual(course.name, "Machine Learning",
            "The name of the course in the DB is not changed")

    def test_exist_course_to_wrong(self) -> None:
        """Submit wrong data to update an existing record."""
        id = 1
        with Database() as db:
            old_course = db.get(id)
        self.assertIsNotNone(old_course,
            f"There is an entry with an ID={id} in the database")
        wrong_data = {
            "name": "Z",
            "start": "03\02\2022",
            "end": "5 Sep 2022",
            "amount": 975
        }
        response = self.client.put(
            "/api/v1/course/%d" % id,
            headers=self.headers,
            data=json.dumps(wrong_data),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
            f"The response status code is `{response.status_code}`")
        self.assertTrue(response.is_json,
            "The response has a valid json format")
        self.assertIn("application/problem+json", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "application/problem+json",
            f"The response MIME type is `{response.mimetype}`")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json",
            f"The response Content-Type header is `{response.content_type}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(error.status, 400,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Bad Request",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

        with Database() as db:
            course = db.get(id)
        self.assertIsNotNone(course,
            "An entry with the specified ID is still exist in the DB")
        self.assertEqual(course.name, "Python forever!",
            "The name of the course in the DB is not changed")


if __name__ == '__main__':
    unittest.main()
