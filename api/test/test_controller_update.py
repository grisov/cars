from flask import json
from api.test import BaseTestCase
from api.models.course import Course
from api.models.error import Error
from api.database import Database


class TestUpdateController(BaseTestCase):
    """Set of tests to check the 'update' controller."""

    def setUp(self) -> None:
        """Performed before each test."""
        self.headers = {
            "Accept": "application/json"
        }
        # Filling the database
        courses = [
            Course("Python forever!", "2021-06-07", "2023-09-27", 44),
            Course("Framework Django", "2022-05-05", "2024-11-19", 25),
            Course("Machine Learning", "2023-06-07", "2025-10-17", 19)
        ]
        db = Database()
        for course in courses:
            db.add(course)
        db.close()

    def tearDown(self) -> None:
        """Performed after each test."""
        self.headers = {}
