import unittest
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
        super(TestGetController, self).setUp()
		        # Filling the database
        courses = [
            Course("Level one", "2021-04-04", "2023-12-22", 37),
            Course("Level two", "2022-05-05", "2024-11-19", 25),
            Course("Level three", "2023-06-07", "2025-10-17", 19)
        ]
        with Database() as db:
            for course in courses:
                db.add(course)

    def test_get_without_parameters(self) -> None:
        """Try to get the entry without specifying the ID."""
        response = self.client.get(
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

    def test_get_existing(self) -> None:
        """Get an existing record."""
        response = self.client.get(
            "/api/v1/course/2",
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
        course = Course(**response.json)
        self.assertEqual(course.name, "Level two",
        f"The name of the course is `{course.name}`")
        self.assertEqual(course.start.isoformat(), "2022-05-05",
        f"The the course will start on `{course.start}`")
        self.assertEqual(course.end.isoformat(), "2024-11-19",
        f"The the course will end on `{course.end}`")
        self.assertEqual(course.amount, 25,
            f"Number of lectures in the course is `{course.amount}`")
        self.assertEqual(course.id, 2,
            f"The ID of the course in the database is `{course.id}`")

        # Check database
        with Database() as db:
            db_course = db.get(2)
        self.assertEqual(db_course, course,
            "The obtained course is identical to the data in the database")

    def test_get_missing(self) -> None:
        """Try to get the missing entry."""
        with Database() as db:
            self.assertIsNone(db.get(789),
                "There is no record for the specified ID in the database")
        response = self.client.get(
            "/api/v1/course/789",
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

    def test_get_using_post(self) -> None:
        """Try to get the entry using POST method."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.post(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        # Check response format
        self.assert405(response,
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
        self.assertEqual(error.status, response.status_code,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Method Not Allowed",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

    def test_get_using_patch(self) -> None:
        """Try to get the entry using PATCH method."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.patch(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        # Check response format
        self.assert405(response,
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
        self.assertEqual(error.status, response.status_code,
            f"The error status code is `{error.status}`")
        self.assertEqual(error.title, "Method Not Allowed",
            f"The error title is `{error.title}`")
        self.assertEqual(error.type, "about:blank",
            f"The error type is `{error.type}`")

    def test_get_headers(self) -> None:
        """Get headers only."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.head(
            "/api/v1/course/1",
            headers=self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
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
        with self.assertRaises(BadRequest):
            course = Course(**response.json)
            error = Error(**response.json)
        self.assertEqual(response.data, b"", "Empty response")


if __name__ == '__main__':
    unittest.main()
