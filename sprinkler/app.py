"""default flask app"""
import json
import logging

from flask import Flask

from sprinkler.control import initialize_relay_gpio
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
    app.logger.info('Loaded zone config: %s', json.dumps(app.config['ZONES'], default=str))# pylint:disable=no-member
    for zone in app.config['ZONES']:
        app.logger.info('Initializing GPIO for zone %s, gpio %s', zone['name'], str(zone['pin']))# pylint:disable=no-member
        initialize_relay_gpio(zone['pin'])
    return app
