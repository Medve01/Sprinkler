from sprinkler import __version__
from tests.fixtures.test_flask_app import client, flask_app

def test_version():
    assert __version__ == '0.1.0'

def test_default_page(client):
    res = client.get('/')
    assert res.status_code == 200
