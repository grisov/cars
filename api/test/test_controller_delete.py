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
        self.headers = {
            "Accept": "application/json"
        }
        # Filling the database
        courses = [
            Course("Level one", "2021-04-04", "2023-12-22", 37),
            Course("Level two", "2022-05-05", "2024-11-19", 25),
            Course("Level three", "2023-06-07", "2025-10-17", 19)
        ]
        db = Database()
        for course in courses:
            db.add(course)
        db.close()

    def tearDown(self) -> None:
        """Performed after each test."""
        self.headers = {}

    def test_delete_existing(self) -> None:
        """Delete an existing record."""
        response = self.client.delete(
            "/api/v1/course/1",
            headers=self.headers
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            error = Error(**response.json)
        course = Course(**response.json)
        self.assertEqual(course.id, 1, "Record ID in DB")
        self.assertEqual(course.name, "Level one", "Course name")
        self.assertEqual(course.start.isoformat(), "2021-04-04", "Start date")
        self.assertEqual(course.end.isoformat(), "2023-12-22", "End date")
        self.assertEqual(course.amount, 37, "Course amount")

    def test_delete_missing(self) -> None:
        """Delete missing record."""
        response = self.client.delete(
            "/api/v1/course/4",
            headers=self.headers
        )
        self.assertStatus(response, 204, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(BadRequest):
            course = Course(**response.json)
            error = Error(**response.json)
        self.assertEqual(response.data, b"", "Empty response")

    def test_delete_without_id(self) -> None:
        """Try to delete the entry
        without specifying the ID.
        """
        response = self.client.delete(
            "/api/v1/course/",
            headers=self.headers
        )
        self.assert404(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/problem+json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Not Found", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_delete_repeatedly(self) -> None:
        """Repeatedly delete record."""
        response = self.client.delete(
            "/api/v1/course/2",
            headers=self.headers
        )
        self.assert200(response, "Status code")
        self.assertEqual(response.json["id"], 2, "ID of the deleted course")

        # Delete record 2 again
        response = self.client.delete(
            "/api/v1/course/2",
            headers=self.headers
        )
        self.assertStatus(response, 204, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(BadRequest):
            course = Course(**response.json)
            error = Error(**response.json)
        self.assertEqual(response.data, b"", "Empty response")


if __name__ == '__main__':
    unittest.main()
