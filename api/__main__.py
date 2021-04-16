#!/usr/bin/env python

import connexion
from api.utils import JSONEncoder


def main() -> None:
    """Create and run Flask application."""
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('spec.yaml',
                arguments={'title': 'Catalog of Courses'},
                pythonic_params=True)
    app.run(port=5000)


if __name__ == '__main__':
    main()
