import pytest
import uuid
import shutil
from os import makedirs
from os.path import exists
from tests.fixtures.test_flask_app import flask_app
from sprinkler.control import get_relay_status, set_relay, initialize_relay_gpio

test_run_id = str(uuid.uuid4())

def test_control_initialize_relay_gpio_already_exported(monkeypatch, flask_app):
    fake_gpio_base = '/tmp/' + test_run_id
    if not exists(fake_gpio_base):
        makedirs(fake_gpio_base)
    if not exists(fake_gpio_base + '/gpio10'):
        makedirs(fake_gpio_base + '/gpio10')
    monkeypatch.setattr('sprinkler.control.GPIO_BASE_PATH', fake_gpio_base)
    with open(fake_gpio_base + '/export', 'w'):
        pass
    with open(fake_gpio_base + '/gpio10/direction', 'w'):
        pass
    with open(fake_gpio_base + '/gpio10/value', 'w'):
        pass
    with flask_app.app_context():
        initialize_relay_gpio('1')
    # with open(fake_gpio_base + '/export', 'r') as f:
    #     content = f.read()
    #     assert content == '10'
    with open(fake_gpio_base + '/gpio10/direction', 'r') as f:
        content = f.read()
        assert content == 'out'
    shutil.rmtree(fake_gpio_base)

def test_control_initialize_relay_gpio_not_exported(monkeypatch, flask_app):
    fake_gpio_base = '/tmp/' + test_run_id
    if not exists(fake_gpio_base):
        makedirs(fake_gpio_base)
    monkeypatch.setattr('sprinkler.control.GPIO_BASE_PATH', fake_gpio_base)
    with open(fake_gpio_base + '/export', 'w'):
        pass
    with flask_app.app_context():
        with pytest.raises(FileNotFoundError):
            initialize_relay_gpio('1')
    with open(fake_gpio_base + '/export', 'r') as f:
        content = f.read()
        assert content == '10'
    shutil.rmtree(fake_gpio_base)


def test_control_get_status(monkeypatch, flask_app):
    fake_gpio_base = '/tmp/' + test_run_id
    if not exists(fake_gpio_base):
        makedirs(fake_gpio_base)
    if not exists(fake_gpio_base + '/gpio10'):
        makedirs(fake_gpio_base + '/gpio10')
    with open(fake_gpio_base + '/gpio10/value', 'w') as f:
        f.write('1')
    if not exists(fake_gpio_base + '/gpio15'):
        makedirs(fake_gpio_base + '/gpio15')
    with open(fake_gpio_base + '/gpio15/value', 'w') as f:
        f.write('0')
    monkeypatch.setattr('sprinkler.control.GPIO_BASE_PATH', fake_gpio_base)
    with flask_app.app_context():
        assert get_relay_status('1') == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': True
            }
        assert get_relay_status('2') == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': False
            }
        assert get_relay_status('3') == None
    shutil.rmtree(fake_gpio_base)


def test_control_set_status(monkeypatch, flask_app):
    fake_gpio_base = '/tmp/' + test_run_id
    if not exists(fake_gpio_base):
        makedirs(fake_gpio_base)
    if not exists(fake_gpio_base + '/gpio10'):
        makedirs(fake_gpio_base + '/gpio10')
    with open(fake_gpio_base + '/gpio10/value', 'w') as f:
        f.write('1')
    if not exists(fake_gpio_base + '/gpio15'):
        makedirs(fake_gpio_base + '/gpio15')
    with open(fake_gpio_base + '/gpio15/value', 'w') as f:
        f.write('0')
    monkeypatch.setattr('sprinkler.control.GPIO_BASE_PATH', fake_gpio_base)
    with flask_app.app_context():
        assert set_relay('1', True) == {
                'id': '1',
                'name': 'test zone 1',
                'pin': 10,
                'on': True
            }
        assert set_relay('2', False) == {
                'id': '2',
                'name': 'test zone 2',
                'pin': 15,
                'on': False
            }
        assert set_relay('3', True) == None
    with open(fake_gpio_base + '/gpio10/value', 'r') as f:
        data = f.read()
        assert bool(int(data)) == True
    with open(fake_gpio_base + '/gpio15/value', 'r') as f:
        data = f.read()
        assert bool(int(data)) == False
    shutil.rmtree(fake_gpio_base)
