import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Garantir que o usuário não está inscrito
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Inscrever
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Não pode inscrever duas vezes
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400

    # Remover inscrição
    response3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response3.status_code == 200
    assert f"Removed {email}" in response3.json()["message"]

    # Não pode remover duas vezes
    response4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response4.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404


def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)  # Pode ser redirect
