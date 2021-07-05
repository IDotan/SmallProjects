from flaskr import models
from flask import Flask

DATABASE = 'url.db'


def create_app():
    """
    | create flask app object
    :return: app object
    """
    models.create_db(DATABASE)
    app = Flask(__name__)
    app.config['DATABASE'] = DATABASE
    from flaskr.views import view
    app.register_blueprint(view)
    return app
