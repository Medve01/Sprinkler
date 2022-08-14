import pytest
import tinydb
from flask import current_app

from sprinkler.sensor import initialize_sensor, sensor_callback

from tests.fixtures.test_flask_app import flask_app

MOCK_CALLED = ""

def test_sensor_callback_no_rain_data(flask_app):
    with flask_app.app_context():
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        # ensure we have no rain data in DB
        events = schedules_db.table('events')
        events.truncate()
        sensor_callback(True)
        event = tinydb.Query()
        rain_data = events.search(event.id == 'had_rain')
        assert len(rain_data) == 1 and rain_data[0]['value'] is True

def test_sensor_callback_rain_data (flask_app):
    with flask_app.app_context():
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        # ensure we have no rain data in DB
        events = schedules_db.table('events')
        events.truncate()
        events.insert({'id': 'had_rain', 'value': False})
        sensor_callback(True)
        event = tinydb.Query()
        rain_data = events.search(event.id == 'had_rain')
        assert len(rain_data) == 1 and rain_data[0]['value'] is True

def mock_gpio_setmode(p):
    pass

def mock_gpio_setup(p1, p2, pull_up_down):
    pass

def mock_gpio_add_event_detect(p1, p2, callback):
    global MOCK_CALLED
    MOCK_CALLED = 'mock_gpio_add_event_detect'

def test_initialize_sensor(monkeypatch, flask_app):
    monkeypatch.setattr('RPi.GPIO.add_event_detect', mock_gpio_add_event_detect)
    with flask_app.app_context():
        initialize_sensor()
    assert MOCK_CALLED == 'mock_gpio_add_event_detect'