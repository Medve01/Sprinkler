import pytest
from sprinkler import __version__
from tests.fixtures.test_flask_app import client, flask_app

def test_version():
    assert __version__ == '0.1.0'

def mock_get_relay_status(zone):
    return {
        'id': zone,
        'name': 'test zone',
        'pin': 10,
        'on': True
    }


def test_default_page(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    res = client.get('/')
    assert res.status_code == 200
