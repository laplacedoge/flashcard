from . import TEMPLATE_DIR
import flask

app = flask.Flask(__name__, template_folder=TEMPLATE_DIR)

basicBlueprint = flask.Blueprint("basicBlueprint", __name__)

@basicBlueprint.route("/upload", methods=["POST"])
def upload():
    return "Hello"
