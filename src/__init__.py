from flask import Flask
from src.extensions import db, ma
from src.config import config_dict


def create_app(config=config_dict['test']):
    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)

    from src.api import api_bp

    app.register_blueprint(api_bp)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)