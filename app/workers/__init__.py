# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("workers", __name__)


from app.workers import routes
