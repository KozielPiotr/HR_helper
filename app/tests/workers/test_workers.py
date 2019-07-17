import pytest
from datetime import datetime

from app.models import Worker
from app.workers.add_worker_utils import add_worker_submit_form, create_worker_start_docs, upgrade_start_docs_status


@pytest.mark.usefixtures("db_session", "context")
def test_add_worker_submit_form(sample_new_worker_form, sample_function, sample_workplace):
    worker_name = sample_new_worker_form.name.data
    worker = Worker.query.filter_by(name=worker_name).first()
    assert not worker
    add_worker_submit_form(sample_new_worker_form)
    worker = Worker.query.filter_by(name=worker_name).first()
    assert worker

    assert worker.name == sample_new_worker_form.name.data
    assert worker.contract_begin == sample_new_worker_form.contract_begin.data
    assert worker.contract_end == sample_new_worker_form.contract_end.data
    assert worker.function_id == sample_function.id
    assert worker.workplace_id == sample_workplace.id

    assert len (Worker.query.filter_by(name=worker_name).all()) == 1
    add_worker_submit_form(sample_new_worker_form)
    assert len(Worker.query.filter_by(name=worker_name).all()) == 1


def test_create_worker_start_docs(sample_start_doc_type, sample_worker):
    worker_name = sample_worker.name
    doc_name = sample_start_doc_type.name
    assert not sample_worker.start_docs
    create_worker_start_docs(worker_name, [doc_name])
    assert sample_worker.start_docs
    assert len(sample_worker.start_docs) == 1
    assert sample_worker.start_docs[0].start_doc_type == sample_start_doc_type.id


def test_upgrade_start_docs_status(sample_start_doc, sample_start_doc_data, sample_start_doc_data_wo_date):
    assert sample_start_doc.notes != sample_start_doc_data[1]["notes"]
    assert sample_start_doc.delivered != sample_start_doc_data[1]["delivered"]
    assert sample_start_doc.sent_to_hr != sample_start_doc_data[1]["sent"]
    assert sample_start_doc.sent_date != datetime.strptime(sample_start_doc_data[1]["sent-date"], "%Y-%m-%d").date()

    upgrade_start_docs_status(sample_start_doc_data)
    assert upgrade_start_docs_status(sample_start_doc_data)
    assert sample_start_doc.notes == sample_start_doc_data[1]["notes"]
    assert sample_start_doc.delivered == sample_start_doc_data[1]["delivered"]
    assert sample_start_doc.sent_to_hr == sample_start_doc_data[1]["sent"]
    assert sample_start_doc.sent_date == datetime.strptime(sample_start_doc_data[1]["sent-date"], "%Y-%m-%d").date()

    upgrade_start_docs_status(sample_start_doc_data_wo_date)
    assert upgrade_start_docs_status(sample_start_doc_data_wo_date)
    assert sample_start_doc.notes == sample_start_doc_data[1]["notes"]
    assert sample_start_doc.delivered == sample_start_doc_data[1]["delivered"]
    assert sample_start_doc.sent_to_hr == sample_start_doc_data[1]["sent"]
    assert sample_start_doc.sent_date is None

    assert not upgrade_start_docs_status(False)
