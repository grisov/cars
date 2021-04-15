#!/usr/bin/env python

import connexion
from connexion.apps.flask_app import FlaskJSONEncoder
from typing import Dict
from api.models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o) -> Dict:
        if isinstance(o, Model):
            dikt = {}
            for attr in o.openapi_types:
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)


def main() -> None:
    """Run Flask application."""
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('spec.yaml',
                arguments={'title': 'Catalog of Courses'},
                pythonic_params=True)
    app.run(port=5000)


if __name__ == '__main__':
    main()
