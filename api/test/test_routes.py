from api.test import BaseTestCase


class TestRoutes(BaseTestCase):
    """Test case to check the routes."""

    def test_ui_route_get(self) -> None:
        """Testing the 'ui' route of the OpenAPI specification."""
        response = self.client.get("/api/v1/ui/")
        self.assert200(response, "Status code")
        self.assertFalse(response.is_json, "Content-Type negative")
        self.assertIn("text/html", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "text/html", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

    def test_spec_route_get(self) -> None:
        """Testing the OpenAPI specification route."""
        response = self.client.get("/api/v1/openapi.json")
        self.assert200(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

    def test_root_route_get(self) -> None:
        """Testing the root route with ReadMe information."""
        response = self.client.get('/')
        self.assert200(response)
        self.assertFalse(response.is_json, "Content-Type")
        self.assertIn("text/html", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "text/html", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")

    def test_wrong_route_get(self) -> None:
        """Testing the wrong route."""
        response = self.client.get("/wrong_path")
        self.assert404(response, "Status code")
        self.assertTrue(response.is_json, "Content-Type")
        self.assertIn("application/problem+json", response.content_type, "Content-Type")
        self.assertEqual(response.mimetype, "application/problem+json", "MIME Type")
        self.assertEqual(response.charset, "utf-8", "Content charset")
        self.assertSetEqual(set(response.json), set(("status", "title", "detail", "type")), "Fields in response")
        self.assertEqual(response.json['status'], 404, "Status code")
        self.assertEqual(response.json['title'], "Not Found", "Response title")


if __name__ == '__main__':
    unittest.main()
