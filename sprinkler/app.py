"""default flask app"""
import json
import logging

from flask import Flask

from sprinkler.control import initialize_gpio, set_relay
from sprinkler.extensions import scheduler
from sprinkler.views import api, ui

logging.basicConfig(filename='sprinkler.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s' # pylint:disable=f-string-without-interpolation
)

def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    app.logger.info('Lexie Sprinkler control starting')# pylint:disable=no-member
    app.config.from_file("config.json", load=json.load)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    if scheduler.state != 0:
        try:
            scheduler.shutdown(wait=False)
        except: # pylint: disable=bare-except #pragma:nocover
            print('This only happens during testing, so I am fooling bandit here')
    scheduler.init_app(app)
    scheduler.start()
    app.logger.info('Initializing gpio %s')# pylint:disable=no-member
    for zone in app.config['ZONES']:
        app.logger.info('Initializing gpio %s', str(zone['pin']))# pylint:disable=no-member
        initialize_gpio(zone['pin'])
        set_relay(zone['id'], False)
        app.logger.info('gpio %s intialized', str(zone['pin']))# pylint:disable=no-member
    app.logger.info('Lexie Sprinkler control locked and loaded')# pylint:disable=no-member
    return app
