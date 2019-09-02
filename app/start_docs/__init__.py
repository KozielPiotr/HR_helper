# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("start_docs", __name__)


from app.start_docs import routes
