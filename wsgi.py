""" wsgi """
from sprinkler.app import create_app  # pragma: nocover

app = create_app() # pragma: nocover

if __name__ == '__main__': # pragma: nocover
    app.run() # pragma: nocover
