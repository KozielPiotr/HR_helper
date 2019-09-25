#-*- coding: utf-8 -*-

import os


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_URI = "DATABASE_URL"


APP_CONFIG = os.environ.get("APP_CONFIG", "Development")
CONFIG_OBJECT = "{}.{}".format(__name__, APP_CONFIG)


class Config(object):

    TESTING = False
    DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "dummy")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URIL", DEFAULT_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


class Development(Config):

    DEBUG = True
