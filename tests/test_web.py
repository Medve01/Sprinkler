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

MOCK_CALLED = {}

def mock_set_relay(zone_id, onoff):
    global MOCK_CALLED
    MOCK_CALLED['function'] = 'mock_set_relay'
    MOCK_CALLED['args'] = (zone_id, onoff)
@pytest.mark.parametrize(
    ('zone_id', 'onoff', 'results'),
    [
        ('1', 'on', ('1', True)),
        ('1', 'off', ('1', False))
    ]
)
def test_default_page_with_params(client, monkeypatch, zone_id, onoff, results):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    monkeypatch.setattr('sprinkler.control.set_relay', mock_set_relay)
    res = client.get('/?zone_id=' + zone_id + '&onoff=' + onoff)
    assert res.status_code == 200
    assert MOCK_CALLED['function'] == 'mock_set_relay'
    assert MOCK_CALLED['args'] == results
