""" Scheduler related stuff"""
import tinydb
from flask import current_app
from shortuuid import uuid

from sprinkler.control import set_relay
from sprinkler.extensions import scheduler


def load_all_schedules():
    """ Loads all schedules from SCHEDULES_DB and creates a job for them in APScheduler """
    with scheduler.app.app_context():
        schedules = get_all_schedules()
        for schedule in schedules:
            scheduler.add_job(
                id = schedule['id'],
                func=set_relay,
                args=[schedule['zone_id'], bool(int(schedule['switch']))],
                trigger='cron',
                day_of_week = schedule['day_of_week'],
                hour = schedule['hour'],
                minute = schedule['minute']
            )


def add_schedule(day_of_week, hour, minute, zone_id, switch):
    """ adds a schedule to database """
    value = {
        'id': uuid(),
        'day_of_week': day_of_week,
        'hour': hour,
        'minute': minute,
        'zone_id': zone_id,
        'switch': switch
    }
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('schedules')
    db_table.insert(value)
    scheduler.add_job(
        id = value['id'],
        func=set_relay,
        args=[value['zone_id'], bool(int(value['switch']))],
        trigger='cron',
        day_of_week = value['day_of_week'],
        hour = value['hour'],
        minute = value['minute']
)
    return value['id']

def get_all_schedules():
    """Fetches all schedules from DB. Returns a list of dicts as retrieved"""
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('schedules')
    return db_table.all()

def remove_schedule(schedule_id):
    """ Removes schedule from database """
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('schedules')
    db_table.remove(tinydb.Query().id == schedule_id)
    scheduler.remove_job(schedule_id)
