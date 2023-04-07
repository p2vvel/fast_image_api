from fastapi.testclient import TestClient
from .utils import app, clean_db
import datetime


client = TestClient(app)


def test_user_create(clean_db):
    response = client.post(
        "/auth/users", json={"username": "pawel", "password": "1234"}
    )

    assert response.status_code == 200
    json = response.json()
    assert json.get("username") == "pawel"
    assert "password" not in json  # there should be no password sent in response
    assert json.get("is_superuser") == False
    assert json.get("is_active") == True
    assert (
        json.get("id") == 1
    )  # TODO: is it good idea to test it? might be dependable on db engine

    # creation and update times should be equal at the creation moment,
    # although there are some minor differences in miliseconds due to default values being taken separately
    created_at = datetime.datetime.fromisoformat(json.get("created_at"))
    updated_at = datetime.datetime.fromisoformat(json.get("updated_at"))
    assert updated_at - created_at < datetime.timedelta(seconds=0.1)


def test_users():
    response = client.get("/auth/users")
    assert response.status_code == 401
