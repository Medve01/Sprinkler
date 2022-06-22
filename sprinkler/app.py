"""default flask app"""
import json
import logging

from flask import Flask

from sprinkler.views import api, ui

logging.basicConfig(filename='sprinkler.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s' # pylint:disable=f-string-without-interpolation
)

def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    app.logger.info('Lexie Sprinkler system locked and loaded')# pylint:disable=no-member
    return app
