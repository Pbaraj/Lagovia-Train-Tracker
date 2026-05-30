from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_short_query_returns_400():
    response = client.get("/departures?q=Br")

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "QUERY_TOO_SHORT"
    assert response.json()["detail"]["minLength"] == 3
    assert response.json()["detail"]["receivedLength"] == 2


def test_empty_query_after_strip_returns_400():
    response = client.get("/departures?q=  ")

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "QUERY_TOO_SHORT"