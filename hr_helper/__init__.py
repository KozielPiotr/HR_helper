#-*- coding: utf-8 -*-
# pylint: disable=wrong-import-position, missing-docstring

from hr_helper.app import app, db
from hr_helper import models

from hr_helper.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from hr_helper.main import bp as main_bp
app.register_blueprint(main_bp)

from hr_helper.workers import bp as workers_bp
app.register_blueprint(workers_bp)

from hr_helper.start_docs import bp as start_docs_bp
app.register_blueprint(start_docs_bp)
