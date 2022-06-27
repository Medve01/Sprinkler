""" wsgi """
from sprinkler.app import create_app  # pragma: nocover
from sprinkler.scheduler import load_all_schedules

app = create_app() # pragma: nocover
load_all_schedules()

if __name__ == '__main__': # pragma: nocover
    app.run() # pragma: nocover
