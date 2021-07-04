from flaskr import models
from flask import Flask
from flaskr.views import view


def create_app():
    """
    | create flask app object
    :return: app object
    """
    models.create_db()
    app = Flask(__name__)
    app.register_blueprint(view)
    return app
