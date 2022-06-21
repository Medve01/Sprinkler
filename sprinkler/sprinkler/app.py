"""default flask app"""
from flask import Flask


def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    @app.route('/')
    def index():
        return 'OK'
    return app
