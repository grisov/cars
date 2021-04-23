from flask import json
from werkzeug.exceptions import BadRequest
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.database import Database


class TestDeleteController(BaseTestCase):
    """Set of tests to check the 'delete' controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        super(TestDeleteController, self).setUp()
        # Filling the database
        courses = [
            Course("Level one", "2021-04-04", "2023-12-22", 37),
            Course("Level two", "2022-05-05", "2024-11-19", 25),
            Course("Level three", "2023-06-07", "2025-10-17", 19)
        ]
        with Database() as db:
            for course in courses:
                db.add(course)

    def test_without_parameters(self) -> None:
        """Request to endpoint without specifying the ID."""
        response = self.client.delete(
            "/api/v1/course/",
            headers=self.headers
        )
        # Check response format
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

        # Check response content
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

    def test_delete_existing(self) -> None:
        """Delete an existing record."""
        with Database() as db:
            db_course = db.get(1)
        response = self.client.delete(
            "/api/v1/course/1",
            headers=self.headers
        )
        # Check response format
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

        # Check response content
        with self.assertRaises(TypeError):
            error = Error(**response.json)
        course = Course(**response.json)
        self.assertEqual(course.name, "Level one",
        f"The name of the deleted course is `{course.name}`")
        self.assertEqual(course.start.isoformat(), "2021-04-04",
        f"The the deleted course will start on `{course.start}`")
        self.assertEqual(course.end.isoformat(), "2023-12-22",
        f"The the deleted course will end on `{course.end}`")
        self.assertEqual(course.amount, 37,
            f"Number of lectures in the deleted course is `{course.amount}`")
        self.assertEqual(course.id, 1,
            f"The ID of the course that was deleted from the database is `{course.id}`")

        # Check database
        self.assertEqual(course, db_course,
            "The deleted course is identical to the one previously obtained from the database")
        with Database() as db:
            self.assertIsNone(db.get(1),
                "There is no data for the specified ID in the database")

    def test_delete_missing(self) -> None:
        """Delete missing record."""
        with Database() as db:
            self.assertIsNone(db.get(4),
                "There is no data for the specified ID in the database")
        response = self.client.delete(
            "/api/v1/course/4",
            headers=self.headers
        )
        # Check response format
        self.assertStatus(response, 204,
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

        # Check response content
        with self.assertRaises(BadRequest):
            course = Course(**response.json)
            error = Error(**response.json)
        self.assertEqual(response.data, b"", "Empty response")

    def test_delete_repeatedly(self) -> None:
        """Repeatedly delete record."""
        with Database() as db:
            self.assertIsNotNone(db.get(2),
                "There is an entry in the database for the specified ID")
        response = self.client.delete(
            "/api/v1/course/2",
            headers=self.headers
        )
        self.assert200(response,
            f"The response status code is `{response.status_code}`")
        self.assertEqual(response.json["id"], 2,
            "The ID of the deleted course is {response.json['id']}")

        # Delete record 2 again
        response = self.client.delete(
            "/api/v1/course/2",
            headers=self.headers
        )
        # Check response format
        self.assertStatus(response, 204,
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

        # Check response content
        with self.assertRaises(BadRequest):
            course = Course(**response.json)
            error = Error(**response.json)
        self.assertEqual(response.data, b"", "Empty response")


if __name__ == '__main__':
    unittest.main()
