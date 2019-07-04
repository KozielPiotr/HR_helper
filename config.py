#-*- coding: utf-8 -*-

import os


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_URI = 'sqlite:///' + os.path.join(PROJECT_DIR, 'app.db')


APP_CONFIG = os.environ.get("APP_CONFIG", "Development")
CONFIG_OBJECT = "{}.{}".format(__name__, APP_CONFIG)


class Config(object):

    TESTING = False
    DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "dummy")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", DEFAULT_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-string"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class Testing(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class Development(Config):

    DEBUG = True
