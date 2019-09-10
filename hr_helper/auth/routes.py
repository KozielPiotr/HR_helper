"""Routes for user authentication"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from hr_helper.auth.forms import LoginForm
from hr_helper.models import User


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs user in
    :return: main page if user is already logged, login page if not
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    title = "HR - logowanie"

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title=title, form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Logs user out
    :return: login page
    """
    logout_user()
    return redirect(url_for("auth.login"))
