import logging
import connexion
from flask_testing import TestCase
from datetime import datetime


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
        app.config["DATABASE"] = "file:%d?mode=memory&cache=shared" % unique
        app.debug = True
        app.testing = True
        return app
