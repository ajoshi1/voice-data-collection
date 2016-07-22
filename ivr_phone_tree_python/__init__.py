from flask import Flask
from ivr_phone_tree_python.config import config_env_files
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine
from sqlalchemy import *
import os
import json
from sqlalchemy.pool import NullPool

def configure_app(new_app, config_name='development'):
    new_app.config.from_object(config_env_files[config_name])

app = Flask(__name__)
import ivr_phone_tree_python.views

enviornment = 'development'
if os.getenv("ENV") is not None:
    enviornment = os.getenv("ENV")

configure_app(app, enviornment)

engine = create_engine(app.config["DATABASE_URI"], poolclass=NullPool)
metadata = MetaData()

log = Table('log', metadata,
    Column('session_id', Text),
    Column('key', Text),
    Column('value', Text),
    Column('url', Text)
)

metadata.create_all(engine)
