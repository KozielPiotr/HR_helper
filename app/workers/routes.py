"""Routes for workers section of main page"""

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.utils.utilities import required_role
from app.models import Workplace, Function
from app.workers import bp
from app.workers import add_worker_utils
from app.workers.forms import NewWorkerForm


@bp.route("/add-workers", methods=["GET", "POST"])
@login_required
def add_worker():
    """Adds new worker to db"""
    required_role(current_user, "user")

    title = "HR - nowy pracownik"

    form = NewWorkerForm()
    form.workplace.choices = [(str(worker), str(worker)) for worker in Workplace.query.all()]
    form.function.choices = [(str(function), str(function)) for function in Function.query.all()]
    if form.validate_on_submit():
        worker = add_worker_utils.add_worker_submit_form(form)
        if worker:
            return redirect(url_for("main.index"))
        flash("Użytkownik {} już istnieje".format(form.name.data))

    return render_template("workers/add_worker.html", title=title, form=form)
