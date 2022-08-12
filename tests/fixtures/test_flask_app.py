""" flask test app fixture """
import pytest
import os
import glob
from sprinkler.app import create_app

@pytest.fixture
def flask_app():
    """flask app fixture"""

    _app = create_app()
    _app.config['ZONES'] = [
            {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'reverse_logic': False
            },
            {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'reverse_logic': True
            }
        ]
    _app.config['RAIN_SENSOR_ENABLED'] = True
    _app.config['RAIN_SENSOR_PIN'] == 17
    _app.config['SCHEDULES_DB'] = '/tmp/schedules.json'
    yield _app
    if os.path.exists(_app.config['SCHEDULES_DB']):
        os.remove(_app.config['SCHEDULES_DB'])
    fakegpio_files = glob.glob('/tmp/gpio*', recursive=False)
    for file in fakegpio_files:
        os.remove(file)
    return _app

@pytest.fixture
def client(flask_app):
    """flask test client fixture"""
    _client = flask_app.test_client()
    return _client
