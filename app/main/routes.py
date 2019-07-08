"""Routes for user main page"""

from flask import render_template
from flask_login import login_required

from app.main import bp


@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """
    Renders main page
    :return: main page if user is logged
    """
    title = "HR - strona główna"
    return render_template("main/main_page.html", title=title)
