"""Relay control through GPIO"""
import time
from os.path import exists

from flask import current_app

GPIO_BASE_PATH = '/sys/class/gpio'

def gpiopath(pin):
    """Constructs the /sys fail path to a gpio pin"""
    return GPIO_BASE_PATH + '/gpio' + str(pin) + '/value'

def initialize_relay_gpio(zone_id):
    """Makes sure that the relevant GPIO port is exported

    Args:
        zone_id (_type_): zone id
    """
    zones = current_app.config['ZONES']
    for zone in zones:
        if zone['id'] == zone_id:
            if not exists(gpiopath(zone['pin'])):
                with open(GPIO_BASE_PATH + '/export', 'w', encoding='UTF-8') as gpio_export:
                    gpio_export.write(str(zone['pin']))
            directionpath = gpiopath(zone['pin']).replace('value', 'direction')
            with open(directionpath, 'w', encoding='UTF-8') as gpio_direction:
                gpio_direction.write('out')
            for _1 in range(2):
                with open(gpiopath(zone['pin']), 'w', encoding='UTF-8') as gpio:
                    gpio.write('1')
                time.sleep(0.3)
                with open(gpiopath(zone['pin']), 'w', encoding='UTF-8') as gpio:
                    gpio.write('0')
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
            gpio = gpiopath(zone['pin'])
            with open(gpio, 'r', encoding='UTF-8') as gpio_file:
                data = gpio_file.read()
            current_app.logger.info('Read gpio %s, value: %s', zone['pin'], data)
            zone['on'] = bool(int(data))
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
            current_app.logger.info('Switching zone ' + zone['name'] + ' ' + str(on))
            gpio = gpiopath(zone['pin'])
            with open(gpio, 'w', encoding='UTF-8') as gpio_file:
                if on:
                    gpio_file.write('1')
                else:
                    gpio_file.write('0')
            zone['on'] = on
            return zone
    return None
