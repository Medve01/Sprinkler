"""default flask app"""
import json
import logging

from flask import Flask

from sprinkler.control import initialize_gpio
from sprinkler.views import api, ui

logging.basicConfig(filename='sprinkler.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s' # pylint:disable=f-string-without-interpolation
)

def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    app.logger.info('Lexie Sprinkler control starting')
    app.config.from_file("config.json", load=json.load)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    app.logger.info('Initializing gpio %s')
    for zone in app.config['ZONES']:
        app.logger.info('Initializing gpio %s', str(zone['pin']))
        initialize_gpio(zone['pin'])
        app.logger.info('gpio %s intialized', str(zone['pin']))
    app.logger.info('Lexie Sprinkler control locked and loaded')# pylint:disable=no-member
    return app
