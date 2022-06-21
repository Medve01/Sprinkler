""" flask test app fixture """
import pytest
from sprinkler.app import create_app

@pytest.fixture
def flask_app():
    """flask app fixture"""
    _app = create_app()
    return _app

@pytest.fixture
def client(flask_app):
    """flask test client fixture"""
    _client = flask_app.test_client()
    return _client
