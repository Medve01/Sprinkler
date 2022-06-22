"""default flask app"""
import json

from flask import Flask

from sprinkler.views import api, ui


def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    return app
