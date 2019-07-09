import pytest

from app import db
from app.models import User, Worker, Function, Role, EventKind, Event, Workplace
from app.tests.utils import create, delete


@pytest.fixture(scope="module")
def db_session():
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture
def sample_user():
    user = User(username="Test")
    user.set_password("test")
    yield create(user)
    delete(user)


@pytest.fixture
def sample_role():
    role = Role(name="admin")
    yield create(role)
    delete(role)


@pytest.fixture
def sample_worker():
    worker = Worker(name="Test")
    yield create(worker)
    delete(worker)


@pytest.fixture
def sample_function():
    function = Function(name="Test")
    yield create(function)
    delete(function)


@pytest.fixture
def sample_event_kind():
    ek = EventKind(name="UW")
    yield create(ek)
    delete(ek)


@pytest.fixture
def sample_event():
    e = Event()
    yield create(e)
    delete(e)


@pytest.fixture
def sample_workplace():
    workplace = Workplace(name="sample_workplace")
    yield create(workplace)
    delete(workplace)