"""Blueprints for UI and API"""
from flask import Blueprint, current_app, jsonify, render_template, request

from sprinkler import control

ui = Blueprint('ui', __name__, url_prefix='/')

@ui.route('/')
def index():
    """ Index page. Renders a page of the zones and their current status """
    zones = []
    args = request.args
    zone_id = args.get('zone_id')
    onoff = args.get('onoff')
    if None not in (zone_id, onoff):
        if onoff == 'on':
            on = True # pylint:disable=invalid-name
        elif onoff == 'off':
            on = False # pylint:disable=invalid-name
        control.set_relay(zone_id, on)
    with current_app.app_context():
        defined_zones = current_app.config['ZONES']
        for defined_zone in defined_zones:
            zones.append(control.get_relay_status(defined_zone['id']))
    return render_template('index.html', zones=zones)


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/zone/<zone_id>', methods=['GET'])
def get_zone(zone_id):
    """ Gets a zone status """
    status = control.get_relay_status(zone_id)
    if status is None:
        return jsonify({'Error': 'Invalid zone id'}), 404
    return jsonify(status)

@api.route('/zone/<zone_id>/<onoff>', methods=['GET'])
def set_zone(zone_id, onoff):
    """ Turns a zone on/off """
    if onoff == 'on':
        on = True # pylint:disable=invalid-name
    elif onoff == 'off':
        on = False # pylint:disable=invalid-name
    else:
        return jsonify({'Error':'Invalid parameter'}), 400
    with current_app.app_context():
        current_app.logger.info('Turning on zone_id' + zone_id)
    status = control.set_relay(zone_id, on)
    if status is None:
        return jsonify({'Error': 'Invalid zone id'}), 404
    return jsonify(status)
