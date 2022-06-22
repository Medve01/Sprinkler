import pytest
from tests.fixtures.test_flask_app import flask_app
from sprinkler.control import get_relay_status, set_relay

class MockDigitalOutputDevice:
    value = 1
    def __init__(self, pin, active_high, initial_value) -> None:
        pass
    def on(self):
        return 1
    def off(self):
        return 0

def test_control_get_status(monkeypatch, flask_app):
    monkeypatch.setattr('sprinkler.control.DigitalOutputDevice', MockDigitalOutputDevice)
    with flask_app.app_context():
        assert get_relay_status('1') == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': True
            }
        assert get_relay_status('2') == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': True
            }
        assert get_relay_status('3') == None

def test_control_set_status(monkeypatch, flask_app):
    monkeypatch.setattr('sprinkler.control.DigitalOutputDevice', MockDigitalOutputDevice)
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