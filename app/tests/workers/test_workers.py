import pytest
from datetime import datetime

from app.models import Worker
from app.workers.workers_utils import add_worker_submit_form, create_worker_start_docs, upgrade_start_docs_status, \
    query_workers, edit_worker_basic_info


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

    assert len(Worker.query.filter_by(name=worker_name).all()) == 1
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


def test_query_workers_works_field(sample_worker, sample_worker_query_form):
    sample_worker_query_form.works.data = "False"
    sample_worker.working = False
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers
    sample_worker.working = True
    workers = query_workers(sample_worker_query_form)
    assert sample_worker not in workers

    sample_worker_query_form.works.data = "True"
    sample_worker.working = True
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers
    sample_worker.working = False
    workers = query_workers(sample_worker_query_form)
    assert sample_worker not in workers

    sample_worker_query_form.works.data = "all"
    sample_worker.working = True
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers
    sample_worker.working = False
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers


def test_query_workers_name_field(sample_worker, sample_worker_query_form):
    sample_worker_query_form.name.data = sample_worker.name
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers

    sample_worker_query_form.name.data = "wrong name"
    workers = query_workers(sample_worker_query_form)
    assert sample_worker not in workers


def test_query_workers_workplace_field(sample_worker, sample_worker_query_form, sample_workplace):
    sample_worker_query_form.workplace.data = sample_workplace.name
    workers = query_workers(sample_worker_query_form)
    assert sample_worker not in workers

    sample_workplace.set_workplace(sample_worker)
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers

    sample_worker_query_form.workplace.data = "all"
    sample_workplace.workers.remove(sample_worker)
    assert sample_worker.workplace != sample_workplace
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers


def test_query_workers_function_field(sample_worker, sample_worker_query_form, sample_function):
    sample_worker_query_form.function.data = sample_function.name
    workers = query_workers(sample_worker_query_form)
    assert sample_worker not in workers

    sample_function.set_function(sample_worker)
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers

    sample_worker_query_form.function.data = "all"
    sample_function.workers.remove(sample_worker)
    assert sample_worker.function != sample_function
    workers = query_workers(sample_worker_query_form)
    assert sample_worker in workers


def test_edit_worker_basic_info(sample_worker, sample_workplace, sample_function):
    data = {
        "worker_id": sample_worker.id,
        "name": sample_worker.name,
        "workplace_id": sample_workplace.id,
        "function_id": sample_function.id,
        "contract_begin": "",
        "contract_end": "",
        "works": "True",
        "work_end": ""
    }

    edit_worker_basic_info(data)
    assert sample_worker.id == data["worker_id"]
    assert sample_worker.name == data["name"]
    assert sample_worker.workplace_id == data["workplace_id"]
    assert sample_worker.function_id == data["function_id"]
    assert sample_worker.contract_begin is None
    assert sample_worker.contract_end is None
    assert sample_worker.working is True
    assert sample_worker.work_end is None

    data["contract_begin"] = "2019-09-29"
    edit_worker_basic_info(data)
    assert sample_worker.contract_begin == datetime.strptime(data["contract_begin"], "%Y-%m-%d").date()

    data["contract_end"] = "2019-12-18"
    edit_worker_basic_info(data)
    assert sample_worker.contract_end == datetime.strptime(data["contract_end"], "%Y-%m-%d").date()

    data["works"] = "False"
    edit_worker_basic_info(data)
    assert sample_worker.working is False

    works = sample_worker.working
    data["works"] = "wrong input"
    edit_worker_basic_info(data)
    assert sample_worker.working == works

    data["work_end"] = "2020-03-14"
    edit_worker_basic_info(data)
    assert sample_worker.work_end == datetime.strptime(data["work_end"], "%Y-%m-%d").date()
