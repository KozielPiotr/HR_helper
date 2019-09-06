#-*- coding: utf-8 -*-
# pylint: disable=invalid-name

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import CONFIG_OBJECT


app = Flask(__name__)
app.config.from_object(CONFIG_OBJECT)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'
