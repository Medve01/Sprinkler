"""Relay control through GPIO"""
import time

from flask import current_app

import RPi.GPIO as gpio


def initialize_gpio(pin):
    """Set GPIO defaults and flash them"""
    gpio.setmode(gpio.BCM)
    gpio.setup(pin, gpio.OUT)
    for _1 in range(2):
        gpio.output(pin, gpio.HIGH)
        time.sleep(0.3)
        gpio.output(pin, gpio.LOW)
        time.sleep(0.3)

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

def set_relay(zone_id, on): #pylint:disable=invalid-name
    """Turns on/off a relay related to a zone

    Args:
        zone_id (str): the zone id from config.json
        on (bool): True if you want to turn the relay on, False of off

    Returns:
        dict: The zone dict from config.json, extended with (bool)'on': True/False for on/off.
            Returns None if zone was not found in config.json
    """
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
