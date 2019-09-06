"""Utilities for 'add_worker' routes"""

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from hr_helper.app import db
from hr_helper.models import Worker, Function, Workplace, StartDoc, StartDocType


def add_worker_submit_form(form):
    """
    Adds new worker to db based on form
    :param form: form for new worker
    """

    worker = Worker()
    worker.name = form.name.data
    worker.contract_begin = form.contract_begin.data
    worker.contract_end = form.contract_end.data

    function = Function.query.filter_by(name=form.function.data).first()
    workplace = Workplace.query.filter_by(name=form.workplace.data).first()

    if not Worker.query.filter_by(name=form.name.data).first():
        if function:
            function.set_function(worker)
        if workplace:
            workplace.set_workplace(worker)
        db.session.add(worker)
        db.session.commit()
        return True, worker.id
    return False, None


def create_worker_start_docs(worker_name, docs):
    """
    Creates db records for chosen documents and assigns them to worker
    :param worker_name: worker's name
    :param docs: names of chosen documents (list of strings)
    """

    worker = Worker.query.filter_by(name=worker_name).first()
    for doc in docs:
        new_doc = StartDoc()
        doc_type = StartDocType.query.filter_by(name=doc).first()
        doc_type.assign_document(new_doc)
        worker.assign_start_doc(new_doc)
        db.session.add_all([worker, new_doc])
    db.session.commit()


def upgrade_start_docs_status(data):
    """
    Checks if form sent correct data. If it did, then upgrades start document's records.
    Else returns false, so js at front inform user about mistake
    :param data: dict from json sent by frontend js script
    :return: url to main page if data is correct. Else returns False
    """

    if data:
        for key in data:
            doc = StartDoc.query.filter_by(id=key).first()
            doc.delivered = data[key]["delivered"]
            doc.sent_to_hr = data[key]["sent"]
            if data[key]["sent-date"] != "":
                doc.sent_date = datetime.strptime(data[key]["sent-date"], "%Y-%m-%d")
            else:
                doc.sent_date = None
            doc.notes = data[key]["notes"]
            db.session.add(doc)
        db.session.commit()
        return True
    return False


def query_workers(form):
    """
    Makes list of workers meeting criteria
    :param form: search criteria
    :return: list of Worker objects
    """

    crit = {}
    if form.name.data != "":
        crit["name"] = form.name.data

    if form.works.data == "False":
        crit["working"] = False
    elif form.works.data == "True":
        crit["working"] = True
    else:
        pass

    if form.workplace.data != "all":
        crit["workplace"] = Workplace.query.filter_by(name=form.workplace.data).first()

    if form.function.data != "all":
        crit["function"] = Function.query.filter_by(name=form.function.data).first()

    if crit:
        workers = Worker.query.filter_by(**crit).all()
    else:
        workers = Worker.query.all()

    return workers


def edit_worker_basic_info(data):
    """
    Upgrades workers basic data
    :param data: dict with data
    :return: True if everything goes right way. Otherwise false
    """

    worker = Worker.query.filter_by(id=data["worker_id"]).first()
    worker.name = data["name"]
    worker.workplace_id = data["workplace_id"]
    worker.function_id = data["function_id"]
    if data["contract_begin"] != "":
        worker.contract_begin = datetime.strptime(data["contract_begin"], "%Y-%m-%d")
    else:
        worker.contract_begin = None

    if data["contract_end"] != "":
        worker.contract_end = datetime.strptime(data["contract_end"], "%Y-%m-%d")
    else:
        worker.contract_end = None

    if data["works"] == "True":
        worker.working = True
    elif data["works"] == "False":
        worker.working = False
    else:
        pass

    if data["work_end"] != "":
        worker.work_end = datetime.strptime(data["work_end"], "%Y-%m-%d")
    else:
        worker.work_end = None

    db.session.add(worker)
    db.session.commit()


def del_worker(worker_id):
    """
    Deletes given worker from database.
    Also removes every related documents and events
    :param worker_id: id of worker to be removed
    :return: True if successful and False if not
    """
    worker = Worker.query.filter_by(id=worker_id).first()
    events = worker.events
    docs = worker.start_docs
    try:
        db.session.delete(worker)
        for event in events:
            db.session.delete(event)
        for doc in docs:
            db.session.delete(doc)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False
