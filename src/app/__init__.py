"""
factory pattern to create a flask app
"""

from typing import Any, Dict

import flask
from flask import Flask
from logging.config import dictConfig


def create_app(app_config: Dict[str, Any]) -> flask.Flask:
    """
    The factory function that creates the Flask app.
    Register all blueprints here
    """
    import logging as log

    log.info(f"Creating a flask app")
    configure_logging(app_config)

    app = Flask(__name__)
    app.config.update(**app_config)

    log.debug(f"Registering the /api blueprint")

    from app.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/")

    try:
        from app.reviewer import reviewer_blueprint
        app.register_blueprint(reviewer_blueprint, url_prefix='/reviewer')
    except ImportError:
        pass  # ignore this import. it's for task reviewers only

    return app


def configure_logging(app_config: Dict[str, Any]):
    """
    http://flask.pocoo.org/docs/1.0/logging/
    "If possible, configure logging before creating the application object.
    """
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': app_config.get('LOG_LEVEL', 'INFO'),
            'handlers': ['wsgi']
        }
    })
