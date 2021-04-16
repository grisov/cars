import logging
import connexion
from flask_testing import TestCase
from api.__main__ import JSONEncoder


class BaseTestCase(TestCase):
    """Basic test case to check the controllers."""

    def create_app(self):
        """Create and return Flask application instance."""
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.json_encoder = JSONEncoder
        app.add_api('spec.yaml', pythonic_params=True)
        return app.app
