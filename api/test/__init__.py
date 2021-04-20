import logging
import connexion
from flask_testing import TestCase


class BaseTestCase(TestCase):
    """Basic test case to check the controllers."""

    def create_app(self) -> connexion.FlaskApp:
        """Create and return Flask application instance.
        :return: the configured Flask app instance
        :rtype: connexion.FlaskApp
        """
        logging.getLogger('__name__').setLevel('ERROR')
        from api import app
        app.config["DATABASE"] = ":memory:"
        app.debug = True
        app.testing = True
        return app
