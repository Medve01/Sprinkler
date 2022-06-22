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