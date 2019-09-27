import pytest
from flask import json, url_for

from hr_helper.models import Worker, StartDocType, StartDoc
from hr_helper.app import app
from hr_helper.tests.routes.utils import login


@pytest.mark.usefixtures("db_session", "sample_user", "context")
def test_add_worker(sample_function, sample_workplace):
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")

        # checking page connection
        resp = client.get("/add-worker", follow_redirects=True)
        assert resp.status_code == 200
        assert "HR - nowy pracownik" in resp.get_data(as_text=True)
        assert "Nowy pracownik" in resp.get_data(as_text=True)

        # checking adding new worker
        assert not Worker.query.filter_by(name="test_new_worker").first()
        resp = client.post("/add-worker", data=dict(name="test_new_worker",
                                                    password="test",
                                                    contract_begin="01.01.2019",
                                                    contract_end="22.01.2018",
                                                    workplace=sample_workplace.name,
                                                    function=sample_function.name),
                           follow_redirects=True)
        worker = Worker.query.filter_by(name="test_new_worker").first()
        assert worker in Worker.query.all()
        assert "Wybierz dokumenty, które musi dostarczyć" in resp.get_data(as_text=True)


@pytest.mark.usefixtures("db_session", "sample_user", "context")
def test_start_docs_required(sample_user, sample_worker, sample_start_doc_type):
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")

        # checking page connection
        resp = client.get("/{}/start-docs-required".format(sample_worker.id))
        assert resp.status_code == 200
        assert "HR - wybór dokumentów do zatrudnienia" in resp.get_data(as_text=True)
        assert "Wybierz dokumenty, które musi dostarczyć" in resp.get_data(as_text=True)

        # checks if list of start document types is displayed
        types = [doc_type.name for doc_type in StartDocType.query.all()]
        assert types
        for doctype in types:
            assert doctype in resp.get_data(as_text=True)


@pytest.mark.usefixtures("db_session", "sample_user", "context")
def test_create_start_docs(sample_user, sample_worker, sample_start_doc_type):
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")

        resp = client.post("/{}/create-start-docs".format(sample_worker.name),
                           data=json.dumps([sample_start_doc_type.name]),
                           content_type="application/json")

        # checking page connection
        assert resp.status_code == 200

        # checking route functionality
        start_doc = StartDoc.query.filter_by(start_doc_type=sample_start_doc_type.id).first()
        assert start_doc in StartDoc.query.all()
        assert start_doc in sample_worker.start_docs


@pytest.mark.usefixtures("db_session", "sample_user", "context")
def test_worker_start_docs_connection_and_get(sample_worker, sample_start_doc, sample_start_doc_type):
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")

        sample_worker.assign_start_doc(sample_start_doc)
        sample_start_doc_type.assign_document(sample_start_doc)

        resp = client.get(url_for("workers.worker_start_docs"), query_string=dict(worker_name=sample_worker.name))
        data = resp.get_data(as_text=True)

        # checking page connection
        assert resp.status_code == 200
        assert "HR - dokumenty główne: {}".format(sample_worker.name) in data
        assert str(sample_start_doc.id) in data
        assert sample_start_doc_type.name in data


@pytest.mark.usefixtures("db_session", "sample_user", "context")
def test_worker_start_docs_post(sample_worker, sample_start_doc, sample_start_doc_type):
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")

        assert not sample_start_doc_type.docs
        resp = client.post(url_for("workers.worker_start_docs"),
                           query_string=dict(worker_name=sample_worker.name),
                           data=dict(doc_type=[sample_start_doc_type.name]),
                           follow_redirects=True)
        data = resp.get_data(as_text=True)
        assert sample_start_doc_type.docs
        assert len(sample_start_doc_type.docs) == 1
        doc = sample_start_doc_type.docs[0]
        assert "{}-delivered".format(doc.id) in data
