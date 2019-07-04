#-*- coding: utf-8 -*-
# pylint: disable=missing-docstring, wrong-import-position, invalid-name

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import CONFIG_OBJECT


app = Flask(__name__)
app.config.from_object(CONFIG_OBJECT)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
