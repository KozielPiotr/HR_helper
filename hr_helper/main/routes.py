"""Routes for workers main page"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from hr_helper.utils.utilities import required_role


bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """
    Renders main page
    :return: main page if workers is logged
    """
    required_role(current_user, "user")

    title = "HR - strona główna"
    return render_template("main/main_page.html", title=title)
