import pytest
from tests.fixtures.test_flask_app import flask_app
from sprinkler.control import get_relay_status, set_relay

def test_control_get_status(monkeypatch, flask_app):
    with flask_app.app_context():
        assert get_relay_status('1') == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': False
            }
        assert get_relay_status('2') == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': False
            }
        assert get_relay_status('3') == None

def test_control_set_status(monkeypatch, flask_app):
    with flask_app.app_context():
        assert set_relay('1', True) == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': True
            }
        assert set_relay('1', False) == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': False
            }
        assert set_relay('3', True) == None