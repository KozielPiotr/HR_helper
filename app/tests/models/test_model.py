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


class TestWorker:

    def test_assign_event(self, sample_worker, sample_event):
        assert sample_event not in sample_worker.events
        sample_worker.assign_event(sample_event)
        assert sample_event in sample_worker.events

    def test_set_workplace(self, sample_worker, sample_workplace):
        assert sample_worker not in sample_workplace.workers
        sample_workplace.set_workplace(sample_worker)
        assert sample_worker in sample_workplace.workers

    def test_assign_start_doc(self, sample_worker, sample_start_doc):
        assert sample_start_doc not in sample_worker.start_docs
        sample_worker.assign_start_doc(sample_start_doc)
        assert sample_start_doc in sample_worker.start_docs


class TestFunction:

    def test_set_function(self, sample_worker, sample_function):
        assert sample_function != sample_worker.function
        sample_function.set_function(sample_worker)
        assert sample_function == sample_worker.function


class TestEvent:

    def test_set_event_kind(self, sample_event_kind, sample_event):
        assert sample_event_kind != sample_event.event_kind
        sample_event_kind.set_kind(sample_event)
        assert sample_event.event_kind == sample_event_kind


class TestStartDocs:

    def test_assign_document(self, sample_start_doc, sample_start_doc_type):
        assert sample_start_doc not in sample_start_doc_type.docs
        sample_start_doc_type.assign_document(sample_start_doc)
        assert sample_start_doc in sample_start_doc_type.docs
