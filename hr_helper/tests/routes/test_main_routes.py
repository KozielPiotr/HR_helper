import pytest
from flask import url_for

from hr_helper.app import app
from hr_helper.tests.routes.utils import login

main_page_cards = {
    "Pracownicy": ["Nowy pracownik", "Wyszukaj pracownika"],
    "Działy": ["Nowy dział", "Edytuj dział", "Usuń dział"],
    "Zdarzenia": ["Stwórz typ zdarzenia", "Nowe zdarzenie", "Lista zdarzeń", "Zestawienie zdarzeń"],
    "Użytkownicy": ["Nowy użytkownik", "Edytuj użytkownika"],
    "Dokumenty główne": ["Nowy dokument", "Edytuj/usuń dokument"]
}


@pytest.mark.usefixtures("db_session", "sample_user")
def test_index():
    client = app.test_client()
    with client:

        # redirect to login if user not logged in
        resp = client.get("/index")
        assert resp.status_code == 302
        resp = client.get("/index", follow_redirects=True)
        assert resp.status_code == 200
        assert "HR - logowanie" in resp.get_data(as_text=True)

        # logs user in and checks if main page is loaded
        resp = login(client=client, username="Test", password="test")
        data = resp.get_data(as_text=True)
        assert resp.status_code == 200
        assert "HR - strona główna" in data

        # checks main page content
        for card in main_page_cards:
            assert card in data
            for section in main_page_cards[card]:
                assert section in data

        # checks navbar content
        assert "GŁÓWNA" in data
        assert "WYLOGUJ Test" in data


@pytest.mark.usefixtures("sample_user")
def test_links():
    client = app.test_client()
    with client:
        login(client=client, username="Test", password="test")
        resp = client.get("/index")
        data = resp.get_data(as_text=True)
        assert url_for("main.index") in data
        assert url_for("auth.logout") in data
        assert url_for("workers.add_worker") in data
        assert url_for("workers.workers_query") in data
        assert url_for("start_docs.new_start_doc_type") in data
        assert url_for("start_docs.list_start_doc_type") in data
