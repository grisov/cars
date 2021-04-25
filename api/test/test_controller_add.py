import unittest
from flask import json
from typing import Optional
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.database import Database


class TestAddController(BaseTestCase):
    """Set of tests to check the 'add' controller."""

    def test_get_without_parameters(self) -> None:
        """Request to the endpoint without parameters."""
        response = self.client.get(
            '/api/v1/add',
            headers=self.headers
        )
        # Check response format
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

        # Check response content
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

    def test_post_with_empty_request_body(self) -> None:
        """Request to the endpoint with empty request body."""
        self.headers["Content-Type"] = "application/json"
        response = self.client.post(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps({}),
            content_type=self.headers["Content-Type"]
        )
        # Check response format
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

        # Check response content
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

    def test_get_with_valid_data(self) -> None:
        """Testing the process of adding an entry via URL with valid data."""
        data = [
            ('name', 'Technologies'),
            ('start', '2021-06-12'),
            ('end', '2021-09-17'),
            ('amount', 20)
        ]
        response = self.client.get(
            '/api/v1/add',
            headers=self.headers,
            query_string=data
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
        self.assertEqual(course.name, "Technologies",
        f"The name of the added course is `{course.name}`")
        self.assertEqual(course.start.isoformat(), "2021-06-12",
        f"The the added course will start on `{course.start}`")
        self.assertEqual(course.end.isoformat(), "2021-09-17",
        f"The the added course will end on `{course.end}`")
        self.assertEqual(course.amount, 20,
            f"Number of lectures in the added course is `{course.amount}`")
        self.assertEqual(course.id, 1,
            f"The course was added to the database with ID=`{course.id}`")

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertEqual(getattr(db_course, "name"), course.name,
            "The name of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "start"), course.start,
            "The start date of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "end"), course.end,
            "The end date of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "amount"), course.amount,
            "The number of lectures of the added course and the data in the DB are same")

    def test_post_with_valid_data(self) -> None:
        """Testing the process of adding an entry via request body with valid data."""
        self.headers["Content-Type"] = "application/json"
        data = {
            'name': 'Python is awesome!',
            'start': '2025-05-05',
            'end': '2027-07-07',
            'amount': 150
        }
        response = self.client.post(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(data),
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
        course = Course(**response.json)
        self.assertEqual(course.name, "Python is awesome!",
        f"The name of the added course is `{course.name}`")
        self.assertEqual(course.start.isoformat(), "2025-05-05",
        f"The the added course will start on `{course.start}`")
        self.assertEqual(course.end.isoformat(), "2027-07-07",
        f"The the added course will end on `{course.end}`")
        self.assertEqual(course.amount, 150,
            f"Number of lectures in the added course is `{course.amount}`")
        self.assertEqual(course.id, 1,
            f"The course was added to the database with ID=`{course.id}`")

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertEqual(getattr(db_course, "name"), course.name,
            "The name of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "start"), course.start,
            "The start date of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "end"), course.end,
            "The end date of the added course and the data in the DB are same")
        self.assertEqual(getattr(db_course, "amount"), course.amount,
            "The number of lectures of the added course and the data in the DB are same")

    def test_get_with_incomplete_data(self) -> None:
        """Testing the process of adding incomplete data via URL."""
        incomplete_data = [
            ('name', 'MongoDB'),
            ('start', '2021-05-01'),
            ('amount', 18)
        ]
        response = self.client.get(
            '/api/v1/add',
            headers=self.headers,
            query_string=incomplete_data
        )
        # Check response format
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

        # Check response content
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_post_with_incomplete_data(self) -> None:
        """Testing the process of adding incomplete data via request body."""
        self.headers["Content-Type"] = "application/json"
        incomplete_data = {
            'name': 'Incomplete course data',
            'end': '2022-04-29',
            'amount': 19
        }
        response = self.client.post(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(incomplete_data),
            content_type=self.headers["Content-Type"]
        )
        # Check response format
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

        # Check response content
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_get_with_wrong_data(self) -> None:
        """Testing the process of adding wrong data via URL."""
        wrong_data = [
            ('name', ''),
            ('start', '12 Mar 2003'),
            ('end', '14\05\2005'),
            ('amount', 0)
        ]
        response = self.client.get(
            '/api/v1/add',
            headers=self.headers,
            query_string=wrong_data
        )
        # Check response format
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

        # Check response content
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_post_with_wrong_data(self) -> None:
        """Testing the process of adding wrong data via request body."""
        self.headers["Content-Type"] = "application/json"
        wrong_data = {
            'name': 'x',
            'start': '07.08.2007',
            'end': '31, 12, 2006',
            'amount': 345
        }
        response = self.client.post(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(wrong_data),
            content_type=self.headers["Content-Type"]
        )
        # Check response format
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

        # Check response content
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_put_method(self) -> None:
        """Testing the request using PUT method."""
        self.headers["Content-Type"] = "application/json"
        data = {
            'name': 'MySQL',
            'start': '2020-02-29',
            'end': '2020-03-31',
            'amount': 7
        }
        response = self.client.put(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(data),
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_patch_method(self) -> None:
        """Testing the request using PATCH method."""
        self.headers["Content-Type"] = "application/json"
        data = {
            'name': 'MySQL',
            'start': '2020-02-29',
            'end': '2020-03-31',
            'amount': 7
        }
        response = self.client.patch(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(data),
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")

    def test_delete_method(self) -> None:
        """Testing the request using DELETE method."""
        self.headers["Content-Type"] = "application/json"
        data = {
            'name': 'MySQL',
            'start': '2020-02-29',
            'end': '2020-03-31',
            'amount': 7
        }
        response = self.client.patch(
            "/api/v1/add",
            headers = self.headers,
            data=json.dumps(data),
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

        # Check database
        with Database() as db:
            db_course = db.get(1)
        self.assertIsNone(db_course,
            "Nothing was added to the empty database")


if __name__ == '__main__':
    unittest.main()
