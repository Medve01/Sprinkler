""" flask test app fixture """
import pytest
from os import makedirs
from os.path import exists
import shutil
from sprinkler.app import create_app

@pytest.fixture
def flask_app(monkeypatch):
    """flask app fixture"""
    monkeypatch.setattr('sprinkler.control.GPIO_BASE_PATH', '/tmp')
    if not exists('/tmp/gpio10'):
        makedirs('/tmp/gpio10')
    if not exists('/tmp/gpio15'):
        makedirs('/tmp/gpio15')
    with open('/tmp/gpio10/value', 'w'):
        pass
    with open('/tmp/gpio10/direction', 'w'):
        pass


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
    shutil.rmtree('/tmp/gpio10')
    shutil.rmtree('/tmp/gpio15')
    return _app

@pytest.fixture
def client(flask_app):
    """flask test client fixture"""
    _client = flask_app.test_client()
    return _client
