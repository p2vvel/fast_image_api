from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, override_get_user
from api import models
from api.database import get_db
from api.dependencies.auth import get_user
import datetime
import re


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_user_create(clean_db):
    input = {"username": "pawel", "password": "1234"}
    response = client.post("/users", json=input)
    assert response.status_code == 200

    json = response.json()
    assert set(json.keys()) == {
        "id",
        "username",
        "is_active",
        "is_superuser",
        "is_pro_user",
        "created_at",
        "updated_at",
        "uuid"
    }
    assert json.get("username") == "pawel"
    assert json.get("is_superuser") is False
    assert json.get("is_pro_user") is False
    assert json.get("is_active") is True
    assert isinstance(json.get("id"), int)
    assert re.match(r"[a-zA-Z\d]{8}-([a-zA-Z\d]{4}-){3}[a-zA-Z\d]{12}", json.get("uuid"))
    # creation and update times should be equal at the creation
    # moment, although there are some minor differences in
    # miliseconds due to default values being taken separately
    created_at = datetime.datetime.fromisoformat(json.get("created_at"))
    updated_at = datetime.datetime.fromisoformat(json.get("updated_at"))
    assert updated_at - created_at < datetime.timedelta(seconds=0.2)


def test_create_user_wrong_input(clean_db):
    # normal user creation
    response = client.post("/users", json={"username": "pawel", "password": "1234"})
    assert response.status_code == 200

    # create duplicated username
    response = client.post("/users", json={"username": "pawel", "password": "1234"})
    assert response.status_code == 409  # endpoint should return 409 (duplicate)

    # create user without password
    response = client.post("/users", json={"username": "pawel2"})
    assert response.status_code == 422

    # create user without username
    response = client.post("/users", json={"username": "pawel3"})
    assert response.status_code == 422

    db = next(override_get_db())  # get db to test its content
    assert len(db.query(models.User).all()) == 1  # only first user was created
