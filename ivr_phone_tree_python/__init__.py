from flask import Flask
from ivr_phone_tree_python.config import config_env_files
import logging
from logging.handlers import RotatingFileHandler

def configure_app(new_app, config_name='development'):
    new_app.config.from_object(config_env_files[config_name])

app = Flask(__name__)
import ivr_phone_tree_python.views

#configure logger
formatter = logging.Formatter(
        "%(asctime)s,%(pathname)s,%(lineno)d,%(levelname)s,%(message)s")
handler = RotatingFileHandler('pingpong.log', maxBytes=250000000, backupCount=25)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

configure_app(app)
