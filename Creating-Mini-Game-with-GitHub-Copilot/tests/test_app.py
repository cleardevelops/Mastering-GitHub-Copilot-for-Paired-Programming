import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data


@pytest.mark.parametrize("choice", ["rock", "paper", "scissors"])
def test_valid_choice_returns_result(client, choice):
    response = client.post("/", data={"choice": choice})
    assert response.status_code == 200
    assert f"You chose <b>{choice}</b>".encode() in response.data
    assert any(r in response.data for r in (b"You win!", b"You lose!", b"It&#39;s a tie!"))


def test_invalid_choice_shows_no_result(client):
    response = client.post("/", data={"choice": "lizard"})
    assert response.status_code == 200
    assert b"You chose" not in response.data


def test_title_from_env(client, monkeypatch):
    monkeypatch.setenv("APP_TITLE", "Test Title")
    response = client.get("/")
    assert b"<h1>Test Title</h1>" in response.data
