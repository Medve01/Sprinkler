""" flask test app fixture """
import pytest
from os import makedirs
from os.path import exists
from sprinkler.app import create_app

@pytest.fixture
def flask_app(monkeypatch):
    """flask app fixture"""

    _app = create_app()
    _app.config['ZONES'] = [
            {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10
            },
            {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15
            }
        ]
    return _app

@pytest.fixture
def client(flask_app):
    """flask test client fixture"""
    _client = flask_app.test_client()
    return _client
