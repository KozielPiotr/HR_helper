"""Routes for workers section of main page"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.models import Workplace, Function, Worker, StartDocType
from app.workers import bp
from app.workers.forms import NewWorkerForm, NewStartDocForm, FilterWorkersForm
from app.utils.utilities import required_role
from app.workers import workers_utils


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
        worker = workers_utils.add_worker_submit_form(form)
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

    title = "HR - wybór dokumentów do zatrudnienia"

    return render_template("workers/worker_select_start_docs.html", title=title, docs=documents, worker=worker)


@bp.route("/<worker_name>/create-start-docs", methods=["GET", "POST"])
@login_required
def create_start_docs(worker_name):
    """
    Creates records in db for each document user choose is required
    :param worker_name: worker's name
    :return: url for worker_start_docs
    """

    required_role(current_user, "user")

    data = request.json
    workers_utils.create_worker_start_docs(worker_name, data)

    return url_for("workers.worker_start_docs", worker_name=worker_name)


@bp.route("/worker_start-docs", methods=["GET", "POST"])
@login_required
def worker_start_docs():
    """
    Here user can check if worker delivered all documents needed for hire
    :return: index page if everything is OK
    """

    required_role(current_user, "user")

    worker_name = request.args.get("worker_name")
    worker = Worker.query.filter_by(name=worker_name).first()

    title = "HR dokumenty główne: {}".format(worker.name)

    form = NewStartDocForm()
    form.doc_type.choices = [(str(doc_type), str(doc_type)) for doc_type in StartDocType.query.all()]

    if form.validate_on_submit():
        doc = form.doc_type.data
        workers_utils.create_worker_start_docs(worker_name, [doc])
        return redirect(url_for("workers.worker_start_docs", worker_name=worker_name))

    return render_template("workers/worker_list_start_docs.html", title=title, docs=worker.start_docs, worker=worker,
                           form=form)


@bp.route("/start-docs-status-upgrade", methods=["GET", "POST"])
@login_required
def start_docs_status_upgrade():
    """
    Checks if data delivered by front is correct and upgrades start documents records
    :return: url to main page if data is correct. Else returns False
    """

    required_role(current_user, "user")

    data = request.json
    response = workers_utils.upgrade_start_docs_status(data)

    if response:
        return {"response": url_for("main.index")}

    return {"response": False}


@bp.route("/workers-query", methods=["GET", "POST"])
@login_required
def workers_query():
    """
    Allows to filter workers which user wants to find
    :return: list of workers meeting requirements
    """

    required_role(current_user, "user")

    title = "HR wyszukaj pracownika"

    form = FilterWorkersForm()
    form.workplace.choices = [(str(workplace), str(workplace)) for workplace in Workplace.query.all()]
    form.workplace.choices.insert(0, ("all", "wszystkie"))
    form.function.choices = [(str(function), str(function)) for function in Function.query.all()]
    form.function.choices.insert(0, ("all", "wszystkie"))
    if form.validate_on_submit():
        workers = workers_utils.query_workers(form)
        return render_template("workers/workers_list.html", workers=workers)

    return render_template("workers/workers_query.html", title=title, form=form)


@bp.route("/show-worker/<worker_id>", methods=["GET", "POST"])
@login_required
def show_worker(worker_id):
    """
    Shows important worker's info and allows to edit it
    :param worker_id: id of chosen worker
    :return: template with worker's info
    """

    required_role(current_user, "user")

    worker = Worker.query.filter_by(id=int(worker_id)).first()
    workplaces = Workplace.query.all()
    functions = Function.query.all()

    title = "HR dane pracownika {}".format(worker.name)

    return render_template("workers/show_worker.html", title=title, worker=worker, workplaces=workplaces,
                           functions=functions)


@bp.route("/edit-worker-basic", methods=["GET", "POST"])
@login_required
def edit_worker_basic():
    """
    Gets json with new workers data and updates records in database.
    Used by app/static/js/workers/edit_worker.js in app/templates/workers/show_worker.html
    :return: url for show_worker view
    """

    required_role(current_user, "user")

    data = request.json
    if not data["OK"]:
        return {"response": False}

    workers_utils.edit_worker_basic_info(data)

    return {"response": url_for("workers.show_worker", worker_id=data["worker_id"])}
