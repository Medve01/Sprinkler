from flask import current_app
import pytest
import tinydb

from sprinkler import scheduler
from tests.fixtures.test_flask_app import flask_app

MOCK_CALLED = {}

def test_add_schedule(flask_app, monkeypatch):
    with flask_app.app_context():
        schedule_id = scheduler.add_schedule(day_of_week='*', hour=10, minute=0, zone_id='1', switch=1)
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        table = schedules_db.table('schedules')
        value = table.search(tinydb.Query().id == schedule_id)
    assert value[0] == {
        'id': schedule_id,
        'day_of_week': '*',
        'hour': 10,
        'minute': 0,
        'zone_id': '1',
        'switch': 1
    }

def test_remove_schedule(flask_app, monkeypatch):
    with flask_app.app_context():
        schedule_id = scheduler.add_schedule(day_of_week='*', hour=10, minute=0, zone_id=1, switch=1)
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        table = schedules_db.table('schedules')
        values = table.search(tinydb.Query().id == schedule_id)
        assert len(values) == 1
        scheduler.remove_schedule(schedule_id)
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        table = schedules_db.table('schedules')
        values = table.search(tinydb.Query().id == schedule_id)
        assert len(values) == 0

def mock_get_all_schedules():
    return [{
        'id': 'asdfasdf',
        'zone_id': '1',
        'switch': 1,
        'day_of_week': '*',
        'hour': '10',
        'minute': '0'
    }]

def mock_scheduler_add_job(id, func, args, trigger, day_of_week, hour, minute):
    global MOCK_CALLED
    MOCK_CALLED = {
        'function': 'scheduler_add_job',
        'params': {
            'id': id,
            'func': func,
            'args': args,
            'trigger': trigger,
            'day_of_week': day_of_week,
            'hour': hour,
            'minute': minute
        }
    }

def test_load_all_schedules(flask_app, monkeypatch):
    monkeypatch.setattr('sprinkler.scheduler.get_all_schedules', mock_get_all_schedules)
    monkeypatch.setattr('sprinkler.extensions.scheduler.add_job', mock_scheduler_add_job)
    scheduler.load_all_schedules()
    assert MOCK_CALLED['function'] == 'scheduler_add_job'
