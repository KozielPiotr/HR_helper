"""Routes for workers section of main page"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.utils.utilities import required_role
from app.models import Workplace, Function, Worker, StartDocType
from app.workers import bp
from app.workers import add_worker_utils
from app.workers.forms import NewWorkerForm


@bp.route("/add-workers", methods=["GET", "POST"])
@login_required
def add_worker():
    """
    Adds new worker to db
    :return: redirects to created worker's start documents or, if worker already exists, gives user info about that
    """
    required_role(current_user, "user")

    title = "HR - nowy pracownik"

    form = NewWorkerForm()
    form.workplace.choices = [(str(worker), str(worker)) for worker in Workplace.query.all()]
    form.function.choices = [(str(function), str(function)) for function in Function.query.all()]
    if form.validate_on_submit():
        worker = add_worker_utils.add_worker_submit_form(form)
        if worker[0]:
            return redirect(url_for("workers.start_docs_required", worker_id=worker[1]))
        flash("Użytkownik {} już istnieje".format(form.name.data))

    return render_template("workers/add_worker.html", title=title, form=form)


@bp.route("/<worker_id>/start-docs-required", methods=["GET", "POST"])
@login_required
def start_docs_required(worker_id):
    """
    Allows to manage start documents of worker
    :param worker_id: worker's db id
    :return: renders template with list of all documents where user can choose which of them are needed to hire eworker
    """
    required_role(current_user, "user")

    worker = Worker.query.filter_by(id=worker_id).first()
    documents = StartDocType.query.order_by(StartDocType.id).all()

    return render_template("workers/worker_select_start_docs.html", title="HR - wybór dokumentów do zatrudnienia",
                           docs=documents, worker=worker)


@bp.route("/<worker_name>/create-start-docs", methods=["GET", "POST"])
@login_required
def create_start_docs(worker_name):
    """
    Creates records in db for each document user choose is required
    :param worker_name: worker's name
    :return: url for worker_start_docs
    """
    data = request.json
    add_worker_utils.create_worker_start_docs(worker_name, data)
    return url_for("workers.worker_start_docs", worker_name=worker_name)


@bp.route("/worker_start-docs", methods=["GET", "POST"])
@login_required
def worker_start_docs():
    """
    Here user can check if worker delivered all documents needed for hire
    :return:
    """
    worker_name = request.args.get("worker_name")
    worker = Worker.query.filter_by(name=worker_name).first()
    # TODO frontend with possibility to change doc's columns vals
    return "Lista dokumentów do zatrudnienia: \n{}".format(worker.start_docs)
