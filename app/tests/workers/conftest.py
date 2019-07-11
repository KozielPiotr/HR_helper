import pytest
from datetime import datetime

from app import app
from app.workers.forms import NewWorkerForm



@pytest.fixture
def sample_new_worker_form(sample_function, sample_workplace):
    form = NewWorkerForm()
    form.name.data = "test_worker"
    form.contract_begin.data = datetime(2019, 1, 1, 0, 0)
    form.contract_end.data = datetime(2019, 1, 1, 0, 0)
    form.function.data = sample_function.name
    form.workplace.data = sample_workplace.name


    yield form


@pytest.fixture(scope="function")
def context():
    ctx = app.app_context()
    yield ctx.push()
    ctx.pop()

@pytest.fixture(scope="function")
def request_context():
    ctx = app.request_context()
    yield ctx.push()
    ctx.pop()
