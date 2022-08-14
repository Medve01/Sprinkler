import json
from tests.fixtures.test_flask_app import client, flask_app

def mock_get_relay_status(zone):
    return {
        'id': zone,
        'name': 'test zone',
        'pin': 10,
        'on': True
    }

def mock_get_relay_status_none(zone):
    return None

def test_zone_status(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    res = client.get('/api/zone/1')
    assert res.status_code == 200
    assert res.json['on'] == True
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status_none)
    res = client.get('/api/zone/1')
    assert res.status_code == 404

def mock_set_relay(zone, on):
    return {
        'id': zone,
        'name': 'test zone',
        'pin': 10,
        'on': on
    }

def mock_set_relay_none(zone, on):
    return None

def test_zone_set_status(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.set_relay', mock_set_relay)
    res = client.get('/api/zone/1/on')
    assert res.status_code == 200
    assert res.json['on'] == True

    res = client.get('/api/zone/1/off')
    assert res.status_code == 200
    assert res.json['on'] == False

    res = client.get('/api/zone/1/lofasz')
    assert res.status_code == 400

    monkeypatch.setattr('sprinkler.control.set_relay', mock_set_relay_none)
    res = client.get('/api/zone/lofasz/on')
    assert res.status_code == 404

def test_zones(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    res = client.get('/api/zone')
    assert res.status_code == 200

def mock_switch(switch_id, enabled=None):
    if enabled is None:
        return True
    else:
        return enabled

def test_switch_get(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.switch', mock_switch)
    res = client.get('/api/switch/irrigation_enabled')
    assert res.status_code == 200
    assert res.json['value'] == True

def test_switch_get_invalid_id(client):
    res = client.get('/api/switch/nonexistent')
    assert res.status_code == 400

def test_switch_put(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.switch', mock_switch)
    res = client.put('/api/switch/irrigation_enabled', data=json.dumps({'value': False}))
    assert res.status_code == 200
    assert res.json['value'] == False

def test_switch_put_invalid_id(client):
    res = client.put('/api/switch/nonexistent', data=json.dumps({'value': False}))
    assert res.status_code == 400
