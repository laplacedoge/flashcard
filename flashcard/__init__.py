def createApp(dbPath: str):
    from . import route
    import flask
    import os

    packageDir = os.path.dirname(os.path.abspath(__file__))
    staticDir = os.path.join(packageDir, "static")
    templateDir = os.path.join(packageDir, "template")

    app = flask.Flask(__name__, static_folder=staticDir,
                                template_folder=templateDir)

    app.config["DATABASE_PATH"] = dbPath

    app.register_blueprint(route.blueprint)

    return app
