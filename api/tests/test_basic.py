from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_main_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello!" in response.text
