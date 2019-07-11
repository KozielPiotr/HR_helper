"""Utilities for 'add_worker' route"""

from app import db

from app.models import Worker, Function, Workplace, StartDoc, StartDocType


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
    :param docs: chosen documents
    """

    worker = Worker.query.filter_by(name=worker_name).first()
    for doc in docs:
        new_doc = StartDoc()
        doc_type = StartDocType.query.filter_by(name=doc).first()
        doc_type.assign_document(new_doc)
        worker.assign_start_doc(new_doc)
        db.session.add_all([worker, new_doc])
    db.session.commit()
