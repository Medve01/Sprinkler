import pytest
import tinydb
from flask import current_app

from tests.fixtures.test_flask_app import flask_app
from sprinkler.control import get_relay_status, set_relay, set_sprinkler

MOCK_CALLED = {}

def test_control_get_status(monkeypatch, flask_app):
    with flask_app.app_context():
        assert get_relay_status('1') == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': False,
                'reverse_logic': False
            }
        assert get_relay_status('2') == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': True,
                'reverse_logic': True
            }
        assert get_relay_status('3') == None

def test_control_set_status(monkeypatch, flask_app):
    with flask_app.app_context():
        assert set_relay('1', True) == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': True,
                'reverse_logic': False
            }
        assert set_relay('1', False) == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': False,
                'reverse_logic': False
            }
        assert set_relay('2', True) == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': True,
                'reverse_logic': True
            }
        assert set_relay('2', False) == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': False,
                'reverse_logic': True
            }
        assert set_relay('3', True) == None

def mock_set_relay(zone_id, on):
    global MOCK_CALLED
    MOCK_CALLED = {'name': 'set_relay', 'params': [zone_id, on]}

def test_set_sprinkler_no_rain_data(monkeypatch, flask_app):
    # If there is no rain data, set_relay must be called
    global MOCK_CALLED
    MOCK_CALLED = {}
    monkeypatch.setattr("sprinkler.control.set_relay", mock_set_relay)
    with flask_app.app_context():
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        # ensure we have no rain data in DB
        events = schedules_db.table('events')
        events.truncate()
        set_sprinkler('1', True)
        assert MOCK_CALLED['name'] == 'set_relay' and MOCK_CALLED['params'] == ['1', True]

def test_set_sprinkler_had_rain(monkeypatch, flask_app):
    # If had_rain == True, set_relay must NOT be called and rain data must be inserted (False)
    global MOCK_CALLED
    MOCK_CALLED = {}
    monkeypatch.setattr("sprinkler.control.set_relay", mock_set_relay)
    with flask_app.app_context():
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        # ensure we have True rain data in DB
        events = schedules_db.table('events')
        events.truncate()
        events.insert({'id': 'had_rain', 'value': True})
        set_sprinkler('1', True)
        assert MOCK_CALLED == {}
        event = tinydb.Query()
        rain_data = events.search(event.id == 'had_rain')
        assert rain_data[0]['value'] is False

def test_sprinkler_no_rain(monkeypatch, flask_app):
    # If had_rain == False, set_relay must be called and rain data must be inserted (False)
    global MOCK_CALLED
    MOCK_CALLED = {}
    monkeypatch.setattr("sprinkler.control.set_relay", mock_set_relay)
    with flask_app.app_context():
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        # ensure we have True rain data in DB
        events = schedules_db.table('events')
        events.truncate()
        events.insert({'id': 'had_rain', 'value': False})
        set_sprinkler('1', True)
        assert MOCK_CALLED['name'] == 'set_relay' and MOCK_CALLED['params'] == ['1', True]
        event = tinydb.Query()
        rain_data = events.search(event.id == 'had_rain')
        assert rain_data[0]['value'] is False