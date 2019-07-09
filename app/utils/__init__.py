# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("utils", __name__)


from app.utils import utilities
