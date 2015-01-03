import os
import logging
from flask import Flask
from dribbble.shots.views import mod as shots_blueprint

app = None


def create_app(*args, **kwargs):
    app = Flask(__name__)
    app.config.from_object('dribbble.conf.local')
    set_logger(app)
    register_blueprints(app)
    return app


def set_logger(app):
    app.logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(
        os.path.join(app.config['LOG_LOCATION'], 'dribbble.log'))
    formatter = logging.Formatter(
        '%(asctime)s  %(levelname)s - %(message)s'
        '[in %(pathname)s:%(lineno)d]')
    logger_handler.setFormatter(formatter)
    app.logger.addHandler(logger_handler)


def register_blueprints(app):
    """Register the our other (non Flask-Restless) blueprints"""
    app.register_blueprint(shots_blueprint)
