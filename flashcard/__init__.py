from .route import basicBlueprint
import flask
import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(PACKAGE_DIR, "template")

def createApp(dbPath: str):
    app = flask.Flask(__name__)

    app.register_blueprint(basicBlueprint)

    return app
