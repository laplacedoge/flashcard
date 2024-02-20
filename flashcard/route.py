from . import database
import flask
import json

blueprint = flask.Blueprint("blueprint", __name__)

@blueprint.route("/")
def index():
    response = flask.render_template("index.html")
    return response

@blueprint.route("/words", methods=["GET", "POST"])
def words():
    dbPath = flask.current_app.config["DATABASE_PATH"]
    dbConn = database.Connection(dbPath)

    max = flask.request.args.get("max", default=10, type=int)
    sort = flask.request.args.get("sort", default="time", type=str)

    sortByTime = True if sort == "time" else False

    method = flask.request.method
    if method == "GET":
        words = dbConn.fetchWords(max, sortByTime)
        response = flask.current_app.response_class(
            response=json.dumps(words),
            mimetype="application/json",
        )
        return response
    elif method == "POST":
        word = flask.request.get_json()
        result = dbConn.insertWord(word)
        response = flask.current_app.response_class(
            response=json.dumps(result),
            mimetype="application/json",
        )
        return response
    else:
        words = []

    return dbPath

@blueprint.route("/words/<int:wordId>", methods=["GET", "PUT", "DELETE"])
def words_detail(wordId: int):
    dbPath = flask.current_app.config["DATABASE_PATH"]
    dbConn = database.Connection(dbPath)

    method = flask.request.method
    if method == "GET":
        result = dbConn.fetchWordById(wordId)
        response = flask.current_app.response_class(
            response=json.dumps(result),
            mimetype="application/json",
        )
        return response
    elif method == "PUT":
        pass
    elif method == "DELETE":
        dbConn.deleteWordById(wordId)
    else:
        return

    return dbPath
