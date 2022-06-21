"""default flask app"""
from flask import Flask
from sprinkler.views import bp

def create_app():
    """Flask application factory
    """
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app
