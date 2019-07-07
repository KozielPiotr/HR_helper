import pytest


@pytest.mark.usefixtures("db_session")
class TestUser:

    def test_set_check_password(self, sample_user):
        sample_password = "test password"
        sample_user.set_password(sample_password)
        assert sample_user.check_password(sample_password)

    def test_assign_role(self, sample_user, sample_role):
        assert sample_role not in sample_user.roles
        sample_user.assign_role(sample_role)
        assert sample_role in sample_user.roles


@pytest.mark.usefixtures("db_session")
class TestWorker:

    def test_assign_event(self, sample_worker, sample_event):
        assert sample_event not in sample_worker.events
        sample_worker.assign_event(sample_event)
        assert sample_event in sample_worker.events


@pytest.mark.usefixtures("db_session")
class TestFunction:

    def test_set_function(self, sample_worker, sample_function):
        assert sample_function != sample_worker.function
        sample_function.set_function(sample_worker)
        assert sample_function == sample_worker.function


@pytest.mark.usefixtures("db_session")
class TestEvent:

    def test_set_event_kind(self, sample_event_kind, sample_event):
        assert sample_event_kind != sample_event.event_kind
        sample_event_kind.set_kind(sample_event)
        assert sample_event.event_kind == sample_event_kind
