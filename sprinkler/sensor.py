""" Rain sensor """
import tinydb
from flask import current_app

import RPi.GPIO as gpio


def sensor_callback(channel): #pylint:disable=unused-argument
    """ gpio callback function - to be called when sensor reports rain (gpio is low) """
    database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
    db_table = database.table('events')
    event = tinydb.Query()
    had_rain = db_table.search(event.id == 'had_rain')
    if len(had_rain) == 0:
        db_table.insert({'id': 'had_rain', 'value': True})
    else:
        db_table.update({'id': 'had_rain', 'value': True}, event.id == 'had_rain')

def initialize_sensor():
    """ Sets up input pin and event callback """
    if current_app.config['RAIN_SENSOR_ENABLED']:
        sensor_pin = current_app.config['RAIN_SENSOR_PIN']
        gpio.setmode(gpio.BCM)
        gpio.setup(sensor_pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(sensor_pin, gpio.FALLING, callback=sensor_callback)
