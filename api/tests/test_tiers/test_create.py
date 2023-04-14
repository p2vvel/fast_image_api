from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, override_get_user
from api import models
from api.database import get_db
from api.dependencies.auth import get_user

from ..utils import create_user, auth_header
from ... import models

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_create_permissions(clean_db):
    db = next(override_get_db())
    username = "pawel"
    create_user(username)
    input = {"name": "New tier", "original_image": False, "transform": False}

    # only admins can create tiers
    response = client.post("/tiers", json=input)
    assert response.status_code == 401
    response = client.post("/tiers", json=input, headers=auth_header(username))
    assert response.status_code == 401
    assert len(db.query(models.Tier).all()) == 0  # no tiers are created


def test_tier_create(clean_db):
    create_user("admin", is_superuser=True)
    header = auth_header("admin")
    input = {"name": "New tier", "original_image": False, "transform": False}

    response = client.post("/tiers", json=input, headers=header)
    assert response.status_code == 200
    json = response.json()
    assert set(json.keys()) == {"id", "name", "original_image", "transform", "created_at"}
    for key in input:
        assert input[key] == json[key]
    assert isinstance(json["id"], int)  # TODO: is it good idea to test?


def test_tier_create_duplicate(clean_db):
    create_user("admin", is_superuser=True)
    header = auth_header("admin")
    input = {"name": "New tier", "original_image": False, "transform": False}

    response = client.post("/tiers", json=input, headers=header)
    assert response.status_code == 200

    # try to create tier with same name again
    response = client.post("/tiers", json=input, headers=header)
    assert response.status_code == 409
