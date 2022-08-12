"""Relay control through GPIO"""
import tinydb
from flask import current_app

import RPi.GPIO as gpio
from sprinkler.extensions import scheduler


def initialize_gpio(pin):
    """Set GPIO defaults and flash them"""
    gpio.setmode(gpio.BCM)
    gpio.setup(pin, gpio.OUT)
    # for _1 in range(2):
    #     gpio.output(pin, gpio.HIGH)
    #     time.sleep(0.3)
    #     gpio.output(pin, gpio.LOW)
    #     time.sleep(0.3)

def get_relay_status(zone_id):
    """Gets a status for a relay related to a sprinkler zone

    Args:
        zone_id (str): the zone id from config.json

    Returns:
        dict: The zone dict from config.json, extended with (bool)'on': True/False for on/off.
            Returns None if zone was not found in config.json
    """
    zones = current_app.config['ZONES']
    for zone in zones:
        if zone['id'] == zone_id:
            gpio.setmode(gpio.BCM)
            gpio.setup(zone['pin'], gpio.OUT)
            output = gpio.input(zone['pin'])
            zone['on'] = bool(output)
            if zone['reverse_logic']:
                zone['on'] = not zone['on']
            return zone
    return None

def set_sprinkler(zone_id, on): #pylint:disable=invalid-name
    """ Starts a sprinkler. Checks if the rain sensor reported rain and if not, turns the relay on
        if the <on> para is off, does not check rain sensor report, just turns off """
    with scheduler.app.app_context():
        database = tinydb.TinyDB(current_app.config['SCHEDULES_DB'])
        events = database.table('events')
        event = tinydb.Query()
        had_rain_result = events.search(event.id == 'had_rain')
        if len(had_rain_result) == 0:
            had_rain = False
        else:
            had_rain = had_rain_result[0]['value']
        if not had_rain:
            #if we didn't have enough rain, we should execute the command
            set_relay(zone_id, on)
        else:
            #Reset event, so next time we will execute
            events.update({'id': 'had_rain', 'value': False}, event.id == 'had_rain')


def set_relay(zone_id, on): #pylint:disable=invalid-name
    """Turns on/off a relay related to a zone

    Args:
        zone_id (str): the zone id from config.json
        on (bool): True if you want to turn the relay on, False of off

    Returns:
        dict: The zone dict from config.json, extended with (bool)'on': True/False for on/off.
            Returns None if zone was not found in config.json
    """
    with scheduler.app.app_context():
        zones = current_app.config['ZONES']
        for zone in zones:
            if zone['id'] == zone_id:
                gpio.setmode(gpio.BCM)
                gpio.setup(zone['pin'], gpio.OUT)
                current_app.logger.info('Switching zone ' + zone['name'] + ' ' + str(on))
                if zone['reverse_logic']:
                    on_value = not on
                else:
                    on_value = on
                if on_value:
                    gpio.output(zone['pin'], gpio.HIGH)
                else:
                    gpio.output(zone['pin'], gpio.LOW)
                zone['on'] = on
                return zone
    return None
