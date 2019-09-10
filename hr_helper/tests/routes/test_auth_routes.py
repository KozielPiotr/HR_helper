import pytest

from hr_helper.app import app
from hr_helper.tests.routes.utils import login, logout


@pytest.mark.usefixtures("db_session", "sample_user")
def test_login_page():
    client = app.test_client()
    with client:

        # checks if login page works
        resp = client.get("/login")
        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert "GŁÓWNA" in data
        assert "ZALOGUJ" in data


def test_login_mechanism(sample_user):
    client = app.test_client()
    with client:

        # checks login with proper data
        resp = login(client=client, username="Test", password="test")
        data = resp.get_data(as_text=True)
        assert resp.status_code == 200
        assert "HR - strona główna" in data


def test_login_wrong_password(sample_user):
    client = app.test_client()
    with client:

        # checks login with wrong username
        resp = login(client=client, username="Wrong", password="test")
        data = resp.get_data(as_text=True)
        assert "HR - logowanie" in data
        assert "Nieprawidłowa nazwa użytkownika lub hasło" in data


def test_login_wrong_username(sample_user):
    client = app.test_client()
    with client:

        # checks login with wrong password
        resp = login(client=client, username="Test", password="wrong")
        data = resp.get_data(as_text=True)
        assert "HR - logowanie" in data
        assert "Nieprawidłowa nazwa użytkownika lub hasło" in data


def test_login_wrong_username_and_password(sample_user):
    client = app.test_client()
    with client:

        # checks login with wrong password and username
        resp = login(client=client, username="Wrong", password="wrong")
        data = resp.get_data(as_text=True)
        assert "HR - logowanie" in data
        assert "Nieprawidłowa nazwa użytkownika lub hasło" in data


def test_logout(sample_user):
    client = app.test_client()
    with client:

        # checks if logging out mechanism works
        login(client=client, username="Test", password="test")
        resp = logout(client)
        data = resp.get_data(as_text=True)
        assert "HR - logowanie" in data
