from flask import json
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error


class TestAddController(BaseTestCase):
    """Set of tests to check the 'add' controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        self.headers = {
            "Accept": "application/json"
        }

    def tearDown(self) -> None:
        """Performed after each test."""
        self.headers = {}

    def test_add_get(self) -> None:
        """Testing the process of adding an entry via URL."""
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
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        course = Course(**response.json)
        self.assertEqual(course.name, "Technologies", "Name value")
        self.assertEqual(course.start.isoformat(), "2021-06-12", "Start date")
        self.assertEqual(course.end.isoformat(), "2021-09-17", "End date")
        self.assertEqual(course.amount, 20, "Amount value")
        self.assertEqual(course.id, 1, "ID value")

    def test_add_post(self) -> None:
        """Testing the process of adding an entry via request body."""
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
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        course = Course(**response.json)
        self.assertEqual(course.name, "Python is awesome!", "Name value")
        self.assertEqual(course.start.isoformat(), "2025-05-05", "Start date")
        self.assertEqual(course.end.isoformat(), "2027-07-07", "End date")
        self.assertEqual(course.amount, 150, "Amount value")
        self.assertEqual(course.id, 1, "ID value")

    def test_incomplete_get(self) -> None:
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
        self.assert400(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Bad Request", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_incomplete_post(self) -> None:
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
        self.assert400(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Bad Request", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_wrong_get(self) -> None:
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
        self.assert400(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Bad Request", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_wrong_post(self) -> None:
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
        self.assert400(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Bad Request", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_put_method(self) -> None:
        """Testing the requests using PUT method."""
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
        self.assert405(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Method Not Allowed", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_patch_method(self) -> None:
        """Testing the requests using PATCH method."""
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
        self.assert405(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Method Not Allowed", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")

    def test_delete_method(self) -> None:
        """Testing the requests using DELETE method."""
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
        self.assert405(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

        with self.assertRaises(TypeError):
            course = Course(**response.json)
        error = Error(**response.json)
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Keys in response")
        self.assertEqual(error.status, response.status_code, "Status code")
        self.assertEqual(error.title, "Method Not Allowed", "Error title")
        self.assertEqual(error.type, "about:blank", "Error type")


if __name__ == '__main__':
    unittest.main()
