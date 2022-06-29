"""Blueprints for UI and API"""
import json

from flask import (Blueprint, current_app, jsonify, redirect, render_template,
                   request)

from sprinkler import control, scheduler

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
    schedules = scheduler.get_all_schedules()
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    switches = ['Turn off', 'Turn on']
    for schedule in schedules:
        temp = schedule['day_of_week']
        if schedule['day_of_week'] != '*':
            schedule['day_of_week'] = days[int(temp)]
        for zone in current_app.config['ZONES']:
            if zone['id'] == schedule['zone_id']:
                schedule['zone_id'] = zone['name']
        schedule['switch'] = switches[int(schedule['switch'])]
    with open('cputemp.json', 'r', encoding='UTF-8') as cputemp_file:
        cpu_temp = json.load(cputemp_file)
    return render_template('index.html', zones=zones, schedules=schedules, cpu_temp=cpu_temp)

@ui.route('/add', methods=['GET'])
def add_schedule_get():
    """ Renders the add schedule page """
    return render_template('add_schedule.html', zones=current_app.config['ZONES'])

@ui.route('/add', methods=['POST'])
def add_schedule_post():
    """ Saves the schedule to DB """
    scheduler.add_schedule(
        day_of_week=request.form.get('day_of_week'),
        hour=request.form.get('hour'),
        minute=request.form.get('minute'),
        zone_id=request.form.get('zone'),
        switch=request.form.get('switch')
    )
    return redirect('/')

@ui.route('/delete', methods=['GET'])
def delete_schedule():
    """ Saves the schedule to DB """
    args = request.args
    scheduler.remove_schedule(args.get('id'))
    return redirect('/')


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
