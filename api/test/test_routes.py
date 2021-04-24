from api.test import BaseTestCase


class TestRoutes(BaseTestCase):
    """Test case to check the routes."""

    def test_ui_route_get(self) -> None:
        """Testing the 'ui' route of the OpenAPI specification."""
        response = self.client.get("/api/v1/ui/")
        # Check response format
        self.assert200(response,
            f"The response status code is `{response.status_code}`")
        self.assertFalse(response.is_json,
            "The response don't has a valid json format")
        self.assertIn("text/html", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "text/html",
            f"The response MIME type is `{response.mimetype}`")
        self.assertIn("text/html", response.headers["Content-Type"],
            f"The response Content-Type header is `{response.headers['Content-Type']}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        # Check response content
        self.assertGreater(len(response.data), 1000,
            f"The length of the response content is {len(response.data)}")

    def test_spec_route_get(self) -> None:
        """Testing the OpenAPI specification route."""
        response = self.client.get("/api/v1/openapi.json")
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
            f"The response Content-Type header is `{response.headers['Content-Type']}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        # Check response content
        self.assertIn("openapi", response.json,
            "Check for the presence of the required parameter in the OpenAPI specification")
        self.assertIn("info", response.json,
            "Check for the presence of the required parameter in the OpenAPI specification")
        self.assertIn("paths", response.json,
            "Check for the presence of the required parameter in the OpenAPI specification")

    def test_root_route_get(self) -> None:
        """Testing the root route with ReadMe information."""
        response = self.client.get('/')
        # Check response format
        self.assert200(response,
            f"The response status code is `{response.status_code}`")
        self.assertFalse(response.is_json,
            "The response don't has a valid json format")
        self.assertIn("text/html", response.content_type,
            f"The response content type is `{response.content_type}`")
        self.assertEqual(response.mimetype, "text/html",
            f"The response MIME type is `{response.mimetype}`")
        self.assertIn("text/html", response.headers["Content-Type"],
            f"The response Content-Type header is `{response.headers['Content-Type']}`")
        self.assertEqual(response.charset, "utf-8",
            f"The response charset is `{response.charset}`")

        # Check response content
        self.assertGreater(len(response.data), 1000,
            f"The length of the response content is {len(response.data)}")

    def test_wrong_route_get(self) -> None:
        """Testing the wrong route."""
        response = self.client.get("/wrong_path")
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
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")),
            f"The response attributes are `{str(list(response.json))}`")
        self.assertEqual(response.json['status'], 404,
            f"The error status code is `{response.json['status']}`")
        self.assertEqual(response.json['title'], "Not Found",
            f"The error title is `{response.json['title']}`")
        self.assertEqual(response.json['type'], "about:blank",
            f"The error type is `{response.json['type']}`")


if __name__ == '__main__':
    unittest.main()
