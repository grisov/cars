from flask import json
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error


class TestGetController(BaseTestCase):
    """Set of tests to check the 'get_details' controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        self.headers = {
            "Accept": "application/json"
        }

    def tearDown(self) -> None:
        """Performed after each test."""
        self.headers = {}
