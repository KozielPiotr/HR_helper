import pytest
from datetime import datetime

from hr_helper.workers.forms import NewWorkerForm, FilterWorkersForm


@pytest.fixture
def sample_new_worker_form(sample_function, sample_workplace):
    form = NewWorkerForm()
    form.name.data = "test_worker"
    form.contract_begin.data = datetime(2019, 1, 1, 0, 0).date()
    form.contract_end.data = datetime(2019, 1, 1, 0, 0).date()
    form.function.data = sample_function.name
    form.workplace.data = sample_workplace.name

    yield form


@pytest.fixture
def sample_start_doc_data():
    data = {
        1: {
            "delivered": True,
            "sent": True,
            "sent-date": "2019-07-25",
            "notes": "sample note"
        }

    }
    yield data


@pytest.fixture
def sample_start_doc_data_wo_date():
    data = {
        1: {
            "delivered": True,
            "sent": True,
            "sent-date": "",
            "notes": "sample note"
        }

    }
    yield data


@pytest.fixture
def sample_worker_query_form():
    form = FilterWorkersForm()
    form.name.data = ""
    form.workplace.data = None
    form.function.data = None
    form.works.data = ""

    yield form
