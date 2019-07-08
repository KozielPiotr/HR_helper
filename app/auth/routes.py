"""Routes for user authentication"""

from flask import redirect, url_for, flash, request
from flask import render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User


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
