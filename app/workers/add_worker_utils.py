"""Utilities for 'add_worker' route"""

from app import db

from app.models import Worker, Function, Workplace


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
        return True
    return False
