from flask import current_app
import pytest
import tinydb

from sprinkler import scheduler
from tests.fixtures.test_flask_app import flask_app


def test_add_schedule(flask_app, monkeypatch):
    with flask_app.app_context():
        schedule_id = scheduler.add_schedule_to_db(day_of_week='*', hour=10, minute=0, zone_id='1', switch=1)
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
        schedule_id = scheduler.add_schedule_to_db(day_of_week='*', hour=10, minute=0, zone_id=1, switch=1)
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        table = schedules_db.table('schedules')
        values = table.search(tinydb.Query().id == schedule_id)
        assert len(values) == 1
        scheduler.remove_schedule(schedule_id)
        schedules_db = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        table = schedules_db.table('schedules')
        values = table.search(tinydb.Query().id == schedule_id)
        assert len(values) == 0
