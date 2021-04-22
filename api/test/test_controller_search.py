from flask import json
from werkzeug.exceptions import BadRequest
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.models.search_data import SearchData
from api.database import Database


class TestSearchController(BaseTestCase):
    """Set of test cases to check the course search controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        super(TestSearchController, self).setUp()
	        # Filling the database
        courses = [
            Course("Level one", "2021-04-04", "2023-12-22", 37),
            Course("The Python 3.10", "2021-08-19", "2022-04-21", 71),
            Course("Level two", "2022-05-05", "2024-11-19", 25),
            Course("Python forever!", "2021-06-07", "2023-09-27", 44),
            Course("Level three", "2023-06-07", "2025-10-17", 19),
            Course("What is the Python?", "2023-03-23", "2023-08-28", 17)
        ]
        db = Database()
        for course in courses:
            db.add(course)
        db.close()

    def test_get_without_parameters(self) -> None:
        """Search request without parameters
        using GET method.
        """
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 6, "Six records are found")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((1,2,3,4,5,6)), "List of IDs of found records")

    def test_get_by_name(self) -> None:
        """Search by full course name
        using GET method.
        """
        query = [
            ("name", "Level two")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 1, "Only one record found")
        course = Course(**response.json[0])
        self.assertEqual(course.id, 3, "Record with ID=3 in DB")

    def test_get_by_name_substr(self) -> None:
        """Search by part of the name
        using GET method.
        """
        query = [
            ("name", "Level")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 3, "Three records are found")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((1, 3, 5)), "List of IDs of found records")

    def test_get_by_name_no_results(self) -> None:
        """Search by name without results
        using GET method.
        """
        query = [
            ("name", "I do not know what I am looking for")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 0, "No records are found")

    def test_get_by_empty_name(self) -> None:
        """Search using empty course name
        using GET method.
        """
        query = [
            ("name", "")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
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

    def test_post_without_parameters(self) -> None:
        """Search request without parameters
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        response = self.client.post(
            "/api/v1/search",
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
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 6, "Six records are found")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((1,2,3,4,5,6)), "List of IDs of found records")

    def test_post_by_name(self) -> None:
        """Search by full course name
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(name="Python forever!")
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 1, "Only one record found")
        course = Course(**response.json[0])
        self.assertEqual(course.id, 4, "Record with ID=4 in DB")

    def test_post_by_name_substr(self) -> None:
        """Search by part of the name
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(name="Python")
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 3, "Three records are found")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((2, 4, 6)), "List of IDs of found records")

    def test_post_by_name_no_results(self) -> None:
        """Search by name without results
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(name="I am going there - I do not know where")
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 0, "No records are found")

    def test_post_by_empty_name(self) -> None:
        """Search using empty course name
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = {"name": ""}
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query),
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

    def test_get_by_start(self) -> None:
        """Search courses beginning from start date
        using GET method.
        """
        query = [
            ("start", "2022-02-22")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 3, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((3,5,6)), "List of IDs of found records")

    def test_get_by_start_wrong(self) -> None:
        """Search courses with start date in wrong format
        using GET method.
        """
        query = [
            ("start", "19.08.2019")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert400(response,
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

    def test_post_by_start(self) -> None:
        """Search courses beginning from start date
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(start="2022-02-22")
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 3, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((3,5,6)), "List of IDs of found records")

    def test_post_by_start_wrong(self) -> None:
        """Search courses with start date in wrong format
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = {
            "start": "25/12/2021"
        }
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
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

    def test_get_before_end(self) -> None:
        """Search for courses that graduate before the end date
        using GET method.
        """
        query = [
            ("end", "2024-04-24")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 4, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((1,2,4,6)), "List of IDs of found records")

    def test_get_before_end_wrong(self) -> None:
        """Search courses with gratuation date in wrong format
        using GET method.
        """
        query = [
            ("end", "29\05\2020")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert400(response,
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

    def test_post_before_end(self) -> None:
        """Search for courses that graduate before the end date
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(end="2024-04-24")
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 4, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((1,2,4,6)), "List of IDs of found records")

    def test_post_before_end_wrong(self) -> None:
        """Search courses with gratuation date in wrong format
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = {
            "end": "20 Apr 2019"
        }
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query),
            content_type=self.headers["Content-Type"]
        )
        self.assert400(response,
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

    def test_get_all_parameters(self) -> None:
        """Search courses via all parameters
        using GET method.
        """
        query = [
            ("name", "Python"),
            ("start", "2021-06-17"),
            ("end", "2024-04-24")
        ]
        response = self.client.get(
            "/api/v1/search",
            headers=self.headers,
            query_string=query
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 2, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((2,6)), "List of IDs of found records")

    def test_post_all_parameters(self) -> None:
        """Search courses via all parameters
        using POST method.
        """
        self.headers["Content-Type"] = "application/json"
        query = SearchData(
            name="Python",
            start="2021-06-17",
            end="2024-04-24"
        )
        response = self.client.post(
            "/api/v1/search",
            headers=self.headers,
            data=json.dumps(query.to_dict()),
            content_type=self.headers["Content-Type"]
        )
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Content type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertIsInstance(response.json, list, "Response is the list")
        self.assertEqual(len(response.json), 2, "All found records")

        # Validation of data
        courses = [Course(**item) for item in response.json]
        ids = [course.id for course in courses]
        self.assertSetEqual(set(ids), set((2,6)), "List of IDs of found records")

    def test_delete(self) -> None:
        """Request to search using DELETE method."""
        response = self.client.delete(
            "/api/v1/search",
            headers=self.headers
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

    def test_put(self) -> None:
        """Request to search using PUT method."""
        response = self.client.put(
            "/api/v1/search",
            headers=self.headers
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

    def test_patch(self) -> None:
        """Request to search using PATCH method."""
        response = self.client.patch(
            "/api/v1/search",
            headers=self.headers
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

    def test_headers(self) -> None:
        """Check only the headers for the search query."""
        response = self.client.head(
            "/api/v1/search",
            headers=self.headers
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
