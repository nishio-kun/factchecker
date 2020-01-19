from flask import Flask
from flask_cors import CORS

# from api.database import db
import api.database as db
import config

from .views.misc import misc
from .views.user import user_router
from .views.distinction import distinction


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config.from_object('config.Config')
    # db.init_app(app)
    db.init_db(app)

    app.register_blueprint(misc, url_prefix='/api')
    app.register_blueprint(user_router, url_prefix='/api')
    app.register_blueprint(distinction, url_prefix='/api')
    return app


app = create_app()
