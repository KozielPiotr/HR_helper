#-*- coding: utf-8 -*-
# pylint: disable=missing-docstring, wrong-import-position, invalid-name

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

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)


from app import models
