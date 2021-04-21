from flask import json
from werkzeug.exceptions import BadRequest
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.database import Database


class TestGetController(BaseTestCase):
    """Set of tests to check the 'get_details' controller."""

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

    def test_get_existing(self) -> None:
        """Get an existing record."""
        response = self.client.get(
            "/api/v1/course/2",
            headers=self.headers
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        course = Course(**response.json)
        self.assertEqual(course.name, "Level two", "Name value")
        self.assertEqual(course.start.isoformat(), "2022-05-05", "Start date")
        self.assertEqual(course.end.isoformat(), "2024-11-19", "End date")
        self.assertEqual(course.amount, 25, "Amount value")
        self.assertEqual(course.id, 2, "ID value")

    def test_get_missing(self) -> None:
        """Try to get the missing entry."""
        response = self.client.get(
            "/api/v1/course/7",
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

    def test_get_without_id(self) -> None:
        """Try to get the entry
        without specifying the ID.
        """
        response = self.client.get(
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

    def test_get_using_post(self) -> None:
        """Try to get the entry using POST method."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.post(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert405(response, "Status code")
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
        self.assertEqual(error.title, "Method Not Allowed", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_get_using_patch(self) -> None:
        """Try to get the entry using PATCH method."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.patch(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert405(response, "Status code")
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
        self.assertEqual(error.title, "Method Not Allowed", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_get_headers(self) -> None:
        """Get headers only."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.head(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
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
