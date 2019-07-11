import pytest

from app.models import Worker
from app.workers.add_worker_utils import add_worker_submit_form


@pytest.mark.usefixtures("db_session", "context")
def test_add_worker_submit_form(sample_new_worker_form, sample_function, sample_workplace):
    worker_name = sample_new_worker_form.name.data
    assert not Worker.query.filter_by(name=worker_name).first()

    add_worker_submit_form(sample_new_worker_form)
    worker = Worker.query.filter_by(name=worker_name).first()
    assert worker

    assert worker.name == sample_new_worker_form.name.data
    assert worker.contract_begin == sample_new_worker_form.contract_begin.data
    assert worker.contract_end == sample_new_worker_form.contract_end.data
    assert worker.function_id == sample_function.id
    assert worker.workplace_id == sample_workplace.id
