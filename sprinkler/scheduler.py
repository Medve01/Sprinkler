""" Scheduler related stuff"""
import tinydb

from shortuuid import uuid

from flask import current_app

def add_schedule_to_db(day_of_week, hour, minute, zone_id, switch):
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
    return value['id']

def get_all_schedules():
    """Fetches all schedules from DB. Returns a list of dicts as retrieved"""
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('schedules')
    return db_table.all()

def remove_schedule(id):
    """ Removes schedule from database """
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('schedules')
    db_table.remove(tinydb.Query().id == id)
