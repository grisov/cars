import connexion
from api.utils import JSONEncoder


def application() -> connexion.FlaskApp:
    """Create Flask application.
    :return: the configured instance of the Flask application
    :rtype: connexion.FlaskApp
    """
    app = connexion.App(__name__, specification_dir='openapi/')
    app.add_api('spec.yaml',
                arguments={'title': 'Catalog of Courses'},
                pythonic_params=True)
    app.app.config.from_object('api.config')
    app.app.json_encoder = JSONEncoder
    app.app.template_folder=app.app.config["TEMPLATE_FOLDER"]
    app.app.static_folder=app.app.config["STATIC_FOLDER"]
    app.app.static_url_path=app.app.config["STATIC_URL_PATH"]
    return app.app


app = application()
from api.views import *
