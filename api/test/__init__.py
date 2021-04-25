import os
import logging
import connexion
from flask_testing import TestCase
from datetime import datetime
from tempfile import gettempdir


class BaseTestCase(TestCase):
    """Basic test case to check the controllers."""

    def create_app(self) -> connexion.FlaskApp:
        """Create and return Flask application instance.
        :return: the configured Flask app instance
        :rtype: connexion.FlaskApp
        """
        logging.disable(logging.CRITICAL)
        from api import app
        # Create a unique shared in memory database for each test separately
        unique = hash((self.id(), datetime.now().timestamp()))
        self.dbfile = os.path.join(gettempdir(), str(unique))
        app.config["DATABASE"] = self.dbfile
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        app.debug = True
        app.testing = True
        return app

    def setUp(self) -> None:
        """Performed before each test."""
        self.headers = {
            "Accept": "application/json"
        }

    def tearDown(self) -> None:
        """Performed after each test."""
        self.headers = {}
        try:
            os.remove(self.dbfile)
        except Exception:
            pass
        self.dbfile = ''
