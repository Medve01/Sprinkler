import pytest
from bs4 import BeautifulSoup
from sprinkler import __version__
from tests.fixtures.test_flask_app import client, flask_app

def test_version():
    assert __version__ == '0.1.0'

def mock_get_relay_status(zone):
    return {
        'id': zone,
        'name': 'test zone',
        'pin': 10,
        'on': True
    }


def test_default_page(client, monkeypatch):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    res = client.get('/')
    assert res.status_code == 200

MOCK_CALLED = {}

def mock_set_relay(zone_id, onoff):
    global MOCK_CALLED
    MOCK_CALLED['function'] = 'mock_set_relay'
    MOCK_CALLED['args'] = (zone_id, onoff)
@pytest.mark.parametrize(
    ('zone_id', 'onoff', 'results'),
    [
        ('1', 'on', ('1', True)),
        ('1', 'off', ('1', False))
    ]
)
def test_default_page_with_params(client, monkeypatch, zone_id, onoff, results):
    monkeypatch.setattr('sprinkler.control.get_relay_status', mock_get_relay_status)
    monkeypatch.setattr('sprinkler.control.set_relay', mock_set_relay)
    res = client.get('/?zone_id=' + zone_id + '&onoff=' + onoff)
    assert res.status_code == 200
    assert MOCK_CALLED['function'] == 'mock_set_relay'
    assert MOCK_CALLED['args'] == results

def mock_get_all_schedules():
    return [
        {
            'day_of_week': '*',
            'hour': 10,
            'minute': 0,
            'zone_id': '1',
            'switch': 1
        },
        {
            'day_of_week': '0',
            'hour': 10,
            'minute': 0,
            'zone_id': '1',
            'switch': 1
        },
        {
            'day_of_week': '2',
            'hour': 10,
            'minute': 0,
            'zone_id': '1',
            'switch': 1
        },
        {
            'day_of_week': '6',
            'hour': 10,
            'minute': 0,
            'zone_id': '1',
            'switch': 0
        },
    ]

def test_default_page_with_schedules(client, monkeypatch):
    monkeypatch.setattr('sprinkler.scheduler.get_all_schedules', mock_get_all_schedules)
    res = client.get('/')
    soup = BeautifulSoup(res.text, 'html.parser')
    schedule_table = soup.find_all('table')[1]
    tds = schedule_table.tbody.contents[1].find_all('td')
    assert tds[0].contents == ['*']
    assert tds[1].contents == ['10:0']
    assert tds[2].contents == ['Turn on test zone 1']

    tds = schedule_table.tbody.contents[3].find_all('td')
    assert tds[0].contents == ['Sunday']
    assert tds[1].contents == ['10:0']
    assert tds[2].contents == ['Turn on test zone 1']

    tds = schedule_table.tbody.contents[5].find_all('td')
    assert tds[0].contents == ['Tuesday']
    assert tds[1].contents == ['10:0']
    assert tds[2].contents == ['Turn on test zone 1']

    tds = schedule_table.tbody.contents[7].find_all('td')
    assert tds[0].contents == ['Saturday']
    assert tds[1].contents == ['10:0']
    assert tds[2].contents == ['Turn off test zone 1']

def test_schedule_add_page(client):
    res = client.get('/add')
    assert res.status_code == 200

def mock_remove_schedule(id):
    global MOCK_CALLED
    MOCK_CALLED = {
        'function': 'remove_schedule',
        'params': {'id': id}
    }

def test_schedule_remove(client, monkeypatch):
    monkeypatch.setattr('sprinkler.scheduler.remove_schedule', mock_remove_schedule)
    res = client.get('/delete?id=asdfasdf')
    assert res.status_code == 302
    assert MOCK_CALLED == {
        'function': 'remove_schedule',
        'params': {'id': 'asdfasdf'}
    }

def mock_add_schedule(day_of_week, hour, minute, zone_id, switch):
    global MOCK_CALLED
    MOCK_CALLED = {
        'function': 'add_schedule',
        'day_of_weel': day_of_week,
        'hour': hour,
        'minute': minute,
        'zone': zone_id,
        'switch': switch
    }

def test_schedule_add(client, monkeypatch):
    monkeypatch.setattr('sprinkler.scheduler.add_schedule', mock_add_schedule)
    res = client.post('/add', data={
        'day_of_week': '*',
        'hour': 10,
        'minute': 0,
        'zone': '1',
        'switch': 1
    })
    assert res.status_code == 302
    assert MOCK_CALLED == {
        'function': 'add_schedule',
        'day_of_weel': '*',
        'hour': '10',
        'minute': '0',
        'zone': '1',
        'switch': '1'
    }
