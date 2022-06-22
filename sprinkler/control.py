"""Relay control through GPIO"""
from flask import current_app
from gpiozero import DigitalOutputDevice


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
            output = DigitalOutputDevice(zone['pin'], active_high=True, initial_value=None)
            zone['on'] = bool(output.value)
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
            output = DigitalOutputDevice(zone['pin'], active_high=True, initial_value=None)
            if on:
                output.on()
            else:
                output.off()
            zone['on'] = on
            return zone
    return None
